"""
Eventually, this will create an application in Snowflake representing an Omnata Plugin, and registers it.
Requires that the Omnata engine app is already installed.

Since Application Objects don't exist yet, currently we create a database and do all the registration stuff ourselves.
In future, it'll create an application capable of registering itself upon install/upgrade.

Deliberately avoids having the user create a python package for their code, since it shouldn't be necessary effort.
Instead we just upload all .py files adjacent to the file containing the plugin class.
"""
import base64
import distutils.core
import inspect
import json
import os
import re
import shutil
import sys
import typing
from pathlib import Path
from typing import Any, List, Literal, Optional

import pydantic.json  # pylint:disable=no-name-in-module
from jinja2 import Environment, FileSystemLoader
from omnata_plugin_runtime.omnata_plugin import OmnataPlugin, PluginInfo, PluginManifest
from snowcli import utils as snowcli_utils
from snowcli.cli.snowpark_shared import snowpark_package
from snowflake.snowpark import Session

PLUGIN_MODULE = "plugin"


class PluginUploader:
    """
    Uploads plugins to a Snowflake account and registers them with the Omnata app.
    """

    def __init__(self, snowflake_connection: Any):
        if snowflake_connection.__class__.__name__ == "SnowflakeConnection":
            builder = Session.builder
            builder._options["connection"] = snowflake_connection
            self.session: Session = builder.create()
        elif snowflake_connection.__class__.__name__ == "Session":
            self.session: Session = snowflake_connection
        else:
            self.session: Session = Session.builder.configs(
                snowflake_connection
            ).create()
        # self.use_content_function = os.environ.get('OMNATA_USE_CONTENT_FUNCTION',None) is not None
        # self.use_directory_table = os.environ.get('OMNATA_USE_DIRECTORY_TABLE',None) is not None
        # self.developer = os.environ.get('OMNATA_PLUGIN_DEVELOPER','Internal')

    def plugin_info_udf_definition(
        self,
        manifest: PluginManifest,
        anaconda_packages: List[str],
        bundled_packages: List[str],
        icon_source: str,
        plugin_class_name: str,
        has_custom_validator: bool,
        plugin_runtime_version: str,
        database_name: Optional[str] = None,
        schema_name: str = "PLUGIN",
        plugin_tier: str = "byo",
    ):
        # convert icon_source to a base64 string
        if icon_source:
            icon_source = base64.b64encode(icon_source.encode("utf-8")).decode("utf-8")
        # custom outbound sync strategies can contain icons, so we need to convert them to base64
        if manifest.supported_outbound_strategies:
            for strategy in manifest.supported_outbound_strategies:
                if strategy.icon_source:
                    strategy.icon_source = base64.b64encode(
                        strategy.icon_source.encode("utf-8")
                    ).decode("utf-8")
        info_object = PluginInfo(
            manifest=manifest,
            anaconda_packages=anaconda_packages,
            bundled_packages=bundled_packages,
            icon_source=icon_source,
            plugin_class_name=plugin_class_name,
            has_custom_validator=has_custom_validator,
            plugin_runtime_version=plugin_runtime_version,
            package_source="function",
            tier=plugin_tier
        )
        return f"""CREATE OR REPLACE FUNCTION {f"{database_name}." if database_name else ''}{schema_name}.OMNATA_PLUGIN_INFO()
  RETURNS OBJECT
  AS
  $$
    PARSE_JSON('{json.dumps(info_object,default=pydantic.json.pydantic_encoder)}')::object
  $$
  ;
        """

    def upload_plugin(
        self,
        plugin_directory: Path,
        database_name: str,
        stage_name: str,
        schema_name: Optional[str] = None,
        is_airbyte: bool = False,
        partner_plugin: bool = False,
    ) -> str:
        """
        Creates a stage and uploads the latest plugin artifacts, Omnata runtime etc.
        If the schema name is not provided, the plugin_id from the manifest will be used.
        The schema name is returned so that upstream processes know where the stage was created.

        Creates a setup script which will create the plugin UDFs:
        1. OMNATA_PLUGIN_INFO() - returns the plugin manifest
        2. UPDATE_API_CONFIGURATION() - Used by Omnata to advise the plugin of any new external access integration
        objects and secret objects. These are stored in the OMNATA_REGISTRATION table.
        2. CONFIGURE_APIS() - Used by Omnata to advise the plugin of any new external access integration
        objects and secret objects. These are stored in the OMNATA_REGISTRATION table.

        The script will also create the stored procs which receive requests from Omnata.
        It uses the information in the OMNATA_REGISTRATION table (if any) to include the necessary
        external access integrations or secrets bindings.
        After plugin installation, the user will grant the plugin's OMNATA_MANAGEMENT role to the Omnata app.
        Then it will become visible to Omnata, and Omnata will create its own application role for the plugin.
        Then the user will grant that application role to the plugin app, and trust will go both ways.
        At this point, the plugin can be registered from the Omnata side.
        Any time there are new secrets or external access integrations, Omnata will call CONFIGURE_APIS to update
        all the procs.
        """
        print(f"Uploading plugin from directory: {plugin_directory}")
        plugin_class: typing.Type[OmnataPlugin]
        plugin_module_file = f"{PLUGIN_MODULE}.py"
        if is_airbyte:
            setup_script = os.path.join(plugin_directory, "setup.py")
            if not os.path.exists(setup_script):
                raise ValueError(f"Did not find a setup.py file at {setup_script}")
            # for Airbyte connectors, the template includes main.py at the root which imports the Source class.
            # We place our wrapper class next to it and it'll find the Airbyte Source
            airbyte_wrapper_file = os.path.join(
                Path(__file__).parent, "airbyte_wrapper.py"
            )
            shutil.copy(
                airbyte_wrapper_file, os.path.join(plugin_directory, plugin_module_file)
            )
            # This root should also contain a setup.py, which we'll generate a requirements.txt file using
            setup = distutils.core.run_setup(setup_script)
            requirements_file_path = os.path.join(plugin_directory, "requirements.txt")
            wrapper_requirements = ["pyyaml"]
            with open(
                requirements_file_path, "w", encoding="utf-8"
            ) as requirements_file:
                for requirement in setup.install_requires + wrapper_requirements:
                    requirements_file.write(f"{requirement}\n")

        if not os.path.exists(os.path.join(plugin_directory, plugin_module_file)):
            raise ValueError(f"File not found: {plugin_module_file}")
        plugin_tier: Literal["byo","free","standard","premium","partner"] = 'byo' # default
        if partner_plugin:
            plugin_tier = 'partner'
        else:
            tier_file = Path(os.path.join(plugin_directory, "tier.txt"))
            if tier_file.exists():
                plugin_tier = tier_file.read_text(encoding="utf-8").strip()
                if plugin_tier not in ["standard","premium","byo","free"]:
                    raise ValueError(f"Invalid tier {plugin_tier} in {tier_file}")
        print(f"Using plugin tier: {plugin_tier}")
        license_url_file = Path(os.path.join(plugin_directory, "license_url.txt"))
        license_url: Optional[str] = (
            license_url_file.read_text(encoding="utf-8").strip()
            if license_url_file.exists()
            else None
        )

        sys.path.append(os.path.abspath(plugin_directory))
        __import__(PLUGIN_MODULE)
        plugin_class = find_omnata_plugin_in_module(PLUGIN_MODULE)
        plugin_class_instance = plugin_class()

        if plugin_class.__name__ == "OmnataPlugin":
            print(
                "Your plugin class must subclass the OmnataPlugin class, using a different class name"
            )
            return

        print(f"Inspecting plugin class: {plugin_class.__name__}")

        if not issubclass(plugin_class, OmnataPlugin):
            print("Your plugin class must subclass the OmnataPlugin class")
            return

        manifest: PluginManifest = plugin_class_instance.get_manifest()
        if schema_name is None:
            schema_name = manifest.plugin_id.upper()
        # do checks first

        icon_file_name = "icon.svg"
        icon_source = None
        if os.path.exists(os.path.join(plugin_directory, icon_file_name)):
            print("Using icon from icon.svg")
            with open(
                os.path.join(plugin_directory, icon_file_name), encoding="utf-8"
            ) as f:
                icon_source = f.read()
        else:
            print("No icon provided, falling back to default")

        print("Creating database, schema and stage for plugin app")
        self.session.sql(f"create database if not exists {database_name}").collect()
        self.session.sql(
            f"create or replace schema {database_name}.{schema_name}"
        ).collect()
        # self.session.sql(f"create or replace stage {database_name}.{schema_name}.PLUGIN_ASSETS ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')").collect()
        self.session.sql(
            f"create or replace stage {database_name}.{schema_name}.{stage_name}"
        ).collect()

        # we have to chdir because snowcli assumes we're in it when packaging
        original_wd = os.getcwd()
        # if is_airbyte:
        #    airbyte_wrapper
        os.chdir(os.path.abspath(plugin_directory))
        if os.path.exists(".packages"):
            shutil.rmtree(".packages")
        if os.path.exists("app.zip"):
            os.remove("app.zip")

        print("Creating Snowpark package for Snowflake")
        snowpark_package(
            pypi_download="yes",
            check_anaconda_for_pypi_deps=True,
            package_native_libraries="ask",
        )
        self.session.sql(
            f"put file://app.zip @{database_name}.{schema_name}.{stage_name} AUTO_COMPRESS=FALSE OVERWRITE=TRUE"
        ).collect()

        if not os.path.exists(".packages"):
            raise ValueError(".packages directory not found after packaging")
        subfolders = [
            f.path
            for f in os.scandir(".packages")
            if f.is_dir() and ".packages/omnata_plugin_runtime-" in f.path
        ]
        if len(subfolders) != 1:
            raise ValueError(
                "Failed to find omnata-plugin-runtime in downloaded package metadata"
            )
        subfolder = subfolders[0]
        regex_matches = re.search(
            r"^.packages/omnata_plugin_runtime-(.*)\.dist-info$", subfolder
        )
        if regex_matches is None:
            raise ValueError(
                "Failed to parse version of omnata-plugin-runtime package from metadata"
            )
        omnata_plugin_runtime_version = regex_matches.group(1)
        anaconda_packages: List[str] = [
            r.name
            for r in snowcli_utils.parse_requirements("requirements.snowflake.txt")
        ]
        other_packages: List[str] = [
            r.name for r in snowcli_utils.parse_requirements("requirements.other.txt")
        ]
        os.chdir(original_wd)
        # icon_file_name_full = os.path.abspath(os.path.join(plugin_directory,icon_file_name))
        # print(f'Loading icon file {icon_file_name_full} into stage')
        # self.session.sql(f"put file://{icon_file_name_full} @{database_name}.{schema_name}.PLUGIN_ASSETS/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE").collect()
        # create the OMNATA_PLUGIN_INFO UDF
        plugin_class_name = plugin_class.__name__
        print("Creating setup script")
        plugin_fqn: str = f"{manifest.developer_id}__{manifest.plugin_id}".upper()

        install_script = "setup_script.sql"
        default_packages = ["dictdiffer", "jinja2", "requests", "pydantic"]
        if len([w for w in other_packages if "snowflake_snowpark_python" in w]) == 0:
            default_packages = default_packages + ["snowflake-snowpark-python"]

        # remove snowflake-connector-python if it's found its way into the anaconda packages
        anaconda_packages = [
            w for w in anaconda_packages if "snowflake-connector-python" not in w
        ]
        has_custom_validator = (
            plugin_class_instance.outbound_record_validator
            is not OmnataPlugin.outbound_record_validator
        )
        packages_to_include = [
            f"'{p}'" for p in list(set(default_packages + anaconda_packages))
        ]
        with open(install_script, "w", encoding="utf-8") as setup_script:
            setup_script.write(
                "create application role if not exists OMNATA_MANAGEMENT;\n"
            )
            setup_script.write("create schema if not exists DATA;\n")
            # this persistent table is used to store the name of the Omnata Application
            setup_script.write(
                """create table if not exists DATA.OMNATA_REGISTRATION(
                                                APPLICATION_NAME varchar,
                                                EXTERNAL_ACCESS_INTEGRATIONS object,
                                                EXTERNAL_ACCESS_INTEGRATIONS_APPLIED object);\n"""
            )
            setup_script.write(
                """
                alter table DATA.OMNATA_REGISTRATION add column if not exists
                        EXTERNAL_ACCESS_INTEGRATIONS object;\n
                alter table DATA.OMNATA_REGISTRATION add column if not exists
                        EXTERNAL_ACCESS_INTEGRATIONS_APPLIED object;\n
                BEGIN
                    merge into data.omnata_registration
                    using (
                        with integrations as (
                            select VALUE::varchar as INTEGRATION_NAME 
                            from data.omnata_registration,
                            TABLE(flatten(input => EXTERNAL_ACCESS_INTEGRATION_NAMES))),
                        other_secrets as (
                            select VALUE::varchar as OTHER_SECRET_NAME 
                            from data.omnata_registration,
                            TABLE(flatten(input => OTHER_SECRETS))),
                        oauth_secrets as (
                            select VALUE::varchar as OAUTH_SECRET_NAME 
                            from data.omnata_registration,
                            TABLE(flatten(input => OAUTH_SECRETS))
                        )
                        select OBJECT_AGG(INTEGRATION_NAME,OBJECT_CONSTRUCT_KEEP_NULL('other_secret',OTHER_SECRET_NAME,'oauth_secret',OAUTH_SECRET_NAME)) as NEW_INTEGRATIONS
                        from integrations i
                        left join other_secrets other 
                            on replace(i.INTEGRATION_NAME,'CONNECTION_EAI_','') = replace(other.OTHER_SECRET_NAME,'CONNECTION_SECRET_OTHER_','')
                        left join oauth_secrets oauth 
                            on replace(i.INTEGRATION_NAME,'CONNECTION_EAI_','') = replace(oauth.OAUTH_SECRET_NAME,'CONNECTION_SECRET_OAUTH_','')
                    )
                    on 1=1
                    when matched then update set EXTERNAL_ACCESS_INTEGRATIONS = NEW_INTEGRATIONS;\n
                EXCEPTION
                    -- ignore the drop error
                    when other then
                    select 1;
                END;
                BEGIN
                    alter table DATA.OMNATA_REGISTRATION drop column EXTERNAL_ACCESS_INTEGRATION_NAMES;\n
                EXCEPTION
                    -- ignore the drop error
                    when other then
                    select 1;
                END;
                BEGIN
                    alter table DATA.OMNATA_REGISTRATION drop column OTHER_SECRETS;\n
                EXCEPTION
                    -- ignore the drop error
                    when other then
                    select 1;
                END;
                BEGIN
                    alter table DATA.OMNATA_REGISTRATION drop column OAUTH_SECRETS;\n
                EXCEPTION
                    -- ignore the drop error
                    when other then
                    select 1;
                END;
                """
            )
            setup_script.write(
                "grant usage on schema DATA to application role OMNATA_MANAGEMENT;\n"
            )
            setup_script.write(
                "grant create secret on schema DATA to application role OMNATA_MANAGEMENT;\n"
            )
            setup_script.write(
                "grant create network rule on schema DATA to application role OMNATA_MANAGEMENT;\n"
            )
            setup_script.write("create or alter versioned schema PLUGIN;\n")
            setup_script.write(
                "grant usage on schema PLUGIN to application role OMNATA_MANAGEMENT;\n"
            )
            setup_script.write(
                self.plugin_info_udf_definition(
                    manifest=manifest,
                    anaconda_packages=anaconda_packages,
                    bundled_packages=other_packages,
                    icon_source=icon_source,
                    plugin_class_name=plugin_class_name,
                    has_custom_validator=has_custom_validator,
                    plugin_runtime_version=omnata_plugin_runtime_version,
                    plugin_tier=plugin_tier
                )
            )
            setup_script.write(
                "grant usage on function PLUGIN.OMNATA_PLUGIN_INFO() to application role OMNATA_MANAGEMENT;\n"
            )
            templates_path = os.path.join(Path(__file__).parent, "jinja_templates")
            environment = Environment(loader=FileSystemLoader(templates_path))
            # These are all the procs/functions which underneath, need to talk to the plugin code and therefore need all the imports available
            for proc_template in [
                "API_LIMITS",
                "SYNC",
                "CONFIGURATION_FORM",
                "CONNECTION_TEST",
                "CONNECTION_FORM",
                "CONSTRUCT_FORM_OPTION",
                "INBOUND_LIST_STREAMS",
                "CREATE_BILLING_EVENTS",
                "NETWORK_ADDRESSES",
                "RETRIEVE_SECRETS",
                "OUTBOUND_RECORD_VALIDATOR",
                "TEST_OAUTH_TOKEN_EXISTS"
            ]:
                template = environment.get_template(f"{proc_template}.sql.jinja")
                content = template.render(
                    {
                        "plugin_fqn": plugin_fqn,
                        "packages": ",".join(packages_to_include),
                        "plugin_class_name": plugin_class_name,
                        "plugin_class_module": PLUGIN_MODULE,
                    }
                )
                setup_script.write(f"{content}\n")
            # These are all the standard procs which do administrative tasks without talking to the plugin code
            for proc_template in [
                "CONFIGURE_APIS",
                "UPDATE_API_CONFIGURATION",
                "PENDING_API_CONFIGURATION",
                "TEST_CALLBACK",
                "CREATE_GENERIC_SECRET_OBJECT",
                "UPDATE_GENERIC_SECRET_OBJECT",
                "CREATE_OAUTH_SECRET_OBJECT",
                "CREATE_NETWORK_RULE_OBJECT",
                "UPDATE_NETWORK_RULE_OBJECT",
                "POST_INSTALL_ACTIONS"
            ]:
                template = environment.get_template(f"{proc_template}.sql.jinja")
                content = template.render({})
                setup_script.write(f"{content}\n")
            # This doesn't seem to bind secrets correctly when run inside the setup script
            #setup_script.write("call PLUGIN.CONFIGURE_APIS();\n")
            # nulling this value will prompt the engine to call CONFIGURE_APIS next time the plugin is used
            setup_script.write(
                "update DATA.OMNATA_REGISTRATION set EXTERNAL_ACCESS_INTEGRATIONS_APPLIED = null;"
            )
            # Look for a folder named 'udf_handlers', and if it exists, package it up and load it into the stage
            # so that it can be referenced by udfs (see next).
            # it is assumed that for plugins, a single handlers artifact will be used for all udfs
            function_handlers_path = os.path.join(plugin_directory, "udf_handlers")
            if os.path.exists(function_handlers_path):
                print("packaging UDF handlers")
                cwd = os.getcwd()
                # switch to directory for packaging
                os.chdir(function_handlers_path)
                if os.path.exists(".packages"):
                    shutil.rmtree(".packages")
                if os.path.exists("udf_handlers.zip"):
                    os.remove("udf_handlers.zip")
                snowpark_package(
                    pypi_download="yes",
                    check_anaconda_for_pypi_deps=True,
                    package_native_libraries="yes",
                )
                # rename app.zip to udf_handlers.zip
                os.rename("app.zip", "udf_handlers.zip")
                print("Uploading handlers zip to stage")
                for path in sorted(Path(".").rglob("udf_handlers.zip")):
                    self.session.sql(
                        f"put file://udf_handlers.zip @{database_name}.{schema_name}.{stage_name} AUTO_COMPRESS=FALSE OVERWRITE=TRUE"
                    ).collect()
                os.chdir(cwd)

            # Look for a folder named 'udfs', and if it exists, load all the functions in it
            functions_path = os.path.join(plugin_directory, "udfs")
            if os.path.exists(functions_path):
                setup_script.write("create or alter versioned schema UDFS;\n")
                print("Adding udfs")
                for path in sorted(Path(functions_path).glob("*.sql")):
                    with open(path, "r", encoding="utf-8") as udf:
                        setup_script.write(udf.read() + "\n")

            # in rare cases, the plugin author might want to do something of their own in the setup script
            # so we allow them to create a file called setup_script.sql and we'll append it to the end of the script
            custom_setup_script = os.path.join(plugin_directory, "custom_setup_script.sql")
            if os.path.exists(custom_setup_script):
                print("Adding custom setup script contents")
                with open(
                    custom_setup_script, "r", encoding="utf-8"
                ) as custom_setup_script:
                    setup_script.write(custom_setup_script.read() + "\n")

            # Upload the configuration streamlit
            setup_script.write("create or alter versioned schema UI;\n")
            setup_script.write(
                "grant usage on schema UI to application role OMNATA_MANAGEMENT;\n"
            )
            setup_script.write(
                """CREATE STREAMLIT if not exists UI."Plugin Configuration"
FROM '/streamlit'
MAIN_FILE = '/plugin_configuration.py';"""
            )

            setup_script.write(
                """GRANT USAGE ON STREAMLIT UI."Plugin Configuration" TO application role OMNATA_MANAGEMENT;\n"""
            )
            setup_script.write("call PLUGIN.POST_INSTALL_ACTIONS();\n")

        print("Uploading plugin streamlit to stage")
        with open(
            "plugin_configuration.py", "w", encoding="utf-8"
        ) as plugin_configuration:
            template = environment.get_template("plugin_configuration.py.jinja")
            content = template.render({})
            plugin_configuration.write(content)
        self.session.sql(
            (
                f"PUT file://plugin_configuration.py @{database_name}.{schema_name}.{stage_name}/streamlit OVERWRITE=TRUE AUTO_COMPRESS = FALSE\n"
            )
        ).collect()
        # delete the file after uploading
        os.remove("plugin_configuration.py")

        print("Uploading setup script to stage")
        self.session.sql(
            (
                f"PUT file://{install_script} @{database_name}.{schema_name}.{stage_name}/scripts OVERWRITE=TRUE AUTO_COMPRESS = FALSE\n"
            )
        ).collect()

        manifest_file_path = Path("manifest.yml")
        with open(manifest_file_path, "w", encoding="utf-8") as manifest_file:
            template = environment.get_template("manifest.yml.jinja")
            content = template.render(
                {
                    "version_name": "1.0.0",
                    "version_label": "Initial",
                    "comment": "Initial release",
                }
            )
            manifest_file.write(content)
        print("Uploading app manifest to stage")
        self.session.sql(
            (
                f"PUT file://{manifest_file_path} @{database_name}.{schema_name}.{stage_name} OVERWRITE=TRUE AUTO_COMPRESS = FALSE\n"
            )
        ).collect()
        # delete the manifest file once it's uploaded to the stage
        os.remove(manifest_file_path)
        # os.remove(install_script)

        # a hidden option to persist the latest plugin info directly into a function somewhere.
        # we do this because we want to be able to update the shared table containing the plugin directory,
        # but plugins are not actually installed in the partner account where prod packaging occurs.
        if os.environ.get("OMNATA_LATEST_PLUGIN_INFO_DATABASE", None) is not None:
            if os.environ.get("OMNATA_LATEST_PLUGIN_INFO_SCHEMA", None) is None:
                raise ValueError(
                    "OMNATA_LATEST_PLUGIN_INFO_SCHEMA must be set if OMNATA_LATEST_PLUGIN_INFO_DATABASE is set"
                )
            if len(os.environ["OMNATA_LATEST_PLUGIN_INFO_DATABASE"]) == 0:
                raise ValueError("OMNATA_LATEST_PLUGIN_INFO_DATABASE cannot be empty")
            if len(os.environ["OMNATA_LATEST_PLUGIN_INFO_SCHEMA"]) == 0:
                raise ValueError("OMNATA_LATEST_PLUGIN_INFO_SCHEMA cannot be empty")
            print(
                f"Persisting plugin info to {os.environ['OMNATA_LATEST_PLUGIN_INFO_DATABASE']}.{os.environ['OMNATA_LATEST_PLUGIN_INFO_SCHEMA']}.OMNATA_PLUGIN_INFO"
            )
            self.session.sql(
                f"""create database if not exists {os.environ['OMNATA_LATEST_PLUGIN_INFO_DATABASE']}"""
            ).collect()
            self.session.sql(
                f"""create schema if not exists {os.environ['OMNATA_LATEST_PLUGIN_INFO_DATABASE']}.{os.environ['OMNATA_LATEST_PLUGIN_INFO_SCHEMA']}"""
            ).collect()
            self.session.sql(
                self.plugin_info_udf_definition(
                    manifest=manifest,
                    anaconda_packages=anaconda_packages,
                    bundled_packages=other_packages,
                    icon_source=icon_source,
                    plugin_class_name=plugin_class_name,
                    has_custom_validator=has_custom_validator,
                    plugin_runtime_version=omnata_plugin_runtime_version,
                    database_name=os.environ["OMNATA_LATEST_PLUGIN_INFO_DATABASE"],
                    schema_name=os.environ["OMNATA_LATEST_PLUGIN_INFO_SCHEMA"],
                    plugin_tier=plugin_tier
                )
            ).collect()
        return schema_name


def find_omnata_plugin_in_module(module_name):
    """
    Searches within a module for subclasses of OmnataPlugin
    """
    found_plugin = None
    for name, obj in inspect.getmembers(sys.modules[module_name]):
        if inspect.isclass(obj):
            if issubclass(obj, OmnataPlugin) and name != "OmnataPlugin":
                if found_plugin is not None:
                    # it's ok if class A extends class B which extends OmnataPlugin
                    # we just don't want class A and B both extending OmnataPlugin, because how would we know which one to use?
                    if issubclass(obj, found_plugin):
                        found_plugin = obj
                    elif issubclass(found_plugin, obj):
                        pass
                    else:
                        raise ValueError(
                            "Found multiple plugins in the same file, please only directly extend the OmnataPlugin class once."
                        )
                else:
                    found_plugin = obj
    if found_plugin is None:
        classes_present = [
            obj
            for name, obj in inspect.getmembers(sys.modules[module_name])
            if inspect.isclass(obj)
        ]
        raise ValueError(
            f"No plugins found. Please create a subclass of OmnataPlugin. Classes found in module: {classes_present}"
        )
    return found_plugin
