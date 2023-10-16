# This is the common file for our CLI. Please keep it clean (as possible)
#
# - Put here any common utility function you consider.
# - If any function is only called within a specific command, consider moving
#   the function to the proper command file.
# - Please, **do not** define commands here.

from copy import deepcopy
from functools import partial
import json
from os import environ, getcwd, getenv, chmod
from enum import Enum
import sys
from typing import Any, Dict, List, Optional, Tuple, Iterable, Union
import uuid
import click
import click.formatting
import re
from pathlib import Path
from urllib.parse import urlparse, urljoin

from click import Context
import humanfriendly
import humanfriendly.tables
from humanfriendly.tables import format_pretty_table
from tinybird.client import (
    TinyB,
    AuthException,
    AuthNoTokenException,
    DoesNotExistException,
    OperationCanNotBePerformed,
    ConnectorNothingToLoad,
)
from sys import version_info
from tinybird.connectors import Connector
from tinybird.datafile import wait_job
from tinybird.datafile import get_current_main_workspace as _get_current_main_workspace

from tinybird.feedback_manager import FeedbackManager

import asyncio
from functools import wraps

from tinybird.config import (
    DEFAULT_LOCALHOST,
    get_config,
    write_config,
    FeatureFlags,
    VERSION,
    SUPPORTED_CONNECTORS,
    PROJECT_PATHS,
    DEFAULT_API_HOST,
    DEFAULT_UI_HOST,
)

import socket
from contextlib import closing

from tinybird.syncasync import async_to_sync
from tinybird.tb_cli_modules.exceptions import (
    CLIAuthException,
    CLIException,
    CLIWorkspaceException,
    CLIConnectionException,
)
from tinybird.tb_cli_modules.telemetry import (
    init_telemetry,
    add_telemetry_event,
    add_telemetry_sysinfo_event,
    flush_telemetry,
    is_ci_environment,
)

SUPPORTED_FORMATS = ["csv", "ndjson", "json", "parquet"]

MAIN_BRANCH = "main"


def create_connector(connector: str, options: Dict[str, Any]):
    # Imported here to improve startup time when the connectors aren't used
    from tinybird.connectors import create_connector as _create_connector, UNINSTALLED_CONNECTORS

    if connector in UNINSTALLED_CONNECTORS:
        raise CLIException(FeedbackManager.error_connector_not_installed(connector=connector))
    return _create_connector(connector, options)


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if version_info[1] >= 7:  # FIXME drop python 3.6 support
            return asyncio.run(f(*args, **kwargs))
        else:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(f(*args, **kwargs))

    return wrapper


def echo_safe_humanfriendly_tables_format_smart_table(data: Iterable[Any], column_names: List[str]) -> None:
    """
    There is a bug in the humanfriendly library: it breaks to render the small table for small terminals
    (`format_robust_table`) if we call format_smart_table with an empty dataset. This catches the error and prints
    what we would call an empty "robust_table".
    """
    try:
        click.echo(humanfriendly.tables.format_smart_table(data, column_names=column_names))
    except ValueError as exc:
        if str(exc) == "max() arg is an empty sequence":
            click.echo("------------")
            click.echo("Empty")
            click.echo("------------")
        else:
            raise exc


def normalize_datasource_name(s: str) -> str:
    s = re.sub(r"[^0-9a-zA-Z_]", "_", s)
    if s[0] in "0123456789":
        return "c_" + s
    return s


def generate_datafile(
    datafile: str, filename: str, data: Optional[bytes], force: Optional[bool] = False, _format: Optional[str] = "csv"
):
    p = Path(filename)
    base = Path("datasources")
    datasource_name = normalize_datasource_name(p.stem)
    if not base.exists():
        base = Path()
    f = base / (datasource_name + ".datasource")
    if not f.exists() or force:
        with open(f"{f}", "w") as ds_file:
            ds_file.write(datafile)
        click.echo(FeedbackManager.success_generated_file(file=f, stem=datasource_name, filename=filename))

        if data:
            # generate fixture
            if (base / "fixtures").exists():
                # Generating a fixture for Parquet files is not so trivial, since Parquet format
                # is column-based. We would need to add PyArrow as a dependency (which is huge)
                # just to analyze the whole Parquet file to extract one single row.
                if _format == "parquet":
                    click.echo(FeedbackManager.warning_parquet_fixtures_not_supported())
                else:
                    f = base / "fixtures" / (p.stem + f".{_format}")
                    newline = b"\n"  # TODO: guess
                    with open(f, "wb") as fixture_file:
                        fixture_file.write(data[: data.rfind(newline)])
                    click.echo(FeedbackManager.success_generated_fixture(fixture=f))
    else:
        click.echo(FeedbackManager.error_file_already_exists(file=f))


async def get_config_and_hosts(ctx: Context, check_token_exists: bool = False) -> Tuple[Dict[str, Any], str, str]:
    """Returns (config, host, ui_host)"""

    config = ctx.ensure_object(dict)["config"]

    if check_token_exists:
        if config.get("token") is None:
            raise AuthNoTokenException

    if "id" not in config:
        config = await _get_config(config["host"], config["token"], load_tb_file=False)

    host = config["host"]
    ui_host = DEFAULT_UI_HOST if host == DEFAULT_API_HOST else host

    return config, host, ui_host


async def get_current_workspace(client, config):
    workspaces: List[Dict[str, Any]] = (await client.user_workspaces()).get("workspaces", [])
    return next((workspace for workspace in workspaces if workspace["id"] == config["id"]), None)


async def get_current_environment(client, config):
    workspaces: List[Dict[str, Any]] = (await client.user_workspaces_and_branches()).get("workspaces", [])
    return next((workspace for workspace in workspaces if workspace["id"] == config["id"]), None)


async def get_current_main_workspace(client, config):
    return await _get_current_main_workspace(client, config)


async def get_current_workspace_branches(client, config):
    current_main_workspace: Dict[str, Any] = await get_current_main_workspace(client, config)
    user_branches: List[Dict[str, Any]] = (await client.user_workspace_branches()).get("workspaces", [])
    all_branches: List[Dict[str, Any]] = (await client.branches()).get("branches", [])
    branches = all_branches + [branch for branch in user_branches if branch not in all_branches]
    return [branch for branch in branches if branch.get("main") == current_main_workspace["id"]]


class CatchAuthExceptions(click.Group):
    """utility class to get all the auth exceptions"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        init_telemetry()
        add_telemetry_sysinfo_event()
        super().__init__(*args, **kwargs)

    def format_epilog(self, ctx: Context, formatter: click.formatting.HelpFormatter) -> None:
        super().format_epilog(ctx, formatter)

        formatter.write_paragraph()
        formatter.write_heading("Telemetry")
        formatter.write_text(
            """
  Tinybird collects anonymous usage data and errors to improve the command
line experience. To opt-out, set TB_CLI_TELEMETRY_OPTOUT environment
variable to '1' or 'true'."""
        )
        formatter.write_paragraph()

    def __call__(self, *args, **kwargs) -> None:
        error_msg: Optional[str] = None
        error_event: str = "error"

        exit_code: int = 0

        try:
            self.main(*args, **kwargs)
        except AuthNoTokenException:
            error_msg = FeedbackManager.error_notoken()
            error_event = "auth_error"
            exit_code = 1
        except AuthException as ex:
            error_msg = FeedbackManager.error_exception(error=str(ex))
            error_event = "auth_error"
            exit_code = 1
        except SystemExit as ex:
            exit_code = int(ex.code) if ex.code else 0
        except Exception as ex:
            error_msg = str(ex)
            exit_code = 1

        if error_msg:
            click.echo(error_msg)
            add_telemetry_event(error_event, error=error_msg)
        flush_telemetry(wait=True)

        sys.exit(exit_code)


def load_connector_config(ctx: Context, connector_name: str, debug: bool, check_uninstalled: bool = False):
    config_file = Path(getcwd()) / f".tinyb_{connector_name}"
    try:
        if connector_name not in ctx.ensure_object(dict):
            with open(config_file) as file:
                config = json.loads(file.read())
            from tinybird.connectors import UNINSTALLED_CONNECTORS

            if check_uninstalled and connector_name in UNINSTALLED_CONNECTORS:
                click.echo(FeedbackManager.warning_connector_not_installed(connector=connector_name))
                return
            ctx.ensure_object(dict)[connector_name] = create_connector(connector_name, config)
    except IOError:
        if debug:
            click.echo(f"** {connector_name} connector not configured")
        pass


def getenv_bool(key: str, default: bool) -> bool:
    v: Optional[str] = getenv(key)
    if v is None:
        return default
    return v.lower() == "true" or v == "1"


def _get_tb_client(token: str, host: str) -> TinyB:
    disable_ssl: bool = getenv_bool("TB_DISABLE_SSL_CHECKS", False)
    return TinyB(token, host, version=VERSION, disable_ssl_checks=disable_ssl, send_telemetry=True)


def create_tb_client(ctx: Context) -> TinyB:
    token = ctx.ensure_object(dict)["config"].get("token", "")
    host = ctx.ensure_object(dict)["config"].get("host", DEFAULT_API_HOST)
    return _get_tb_client(token, host)


async def _analyze(filename: str, client: TinyB, format: str, connector: Optional[Connector] = None):
    data: Optional[bytes] = None
    if not connector:
        parsed = urlparse(filename)
        if parsed.scheme in ("http", "https"):
            meta = await client.datasource_analyze(filename)
        else:
            with open(filename, "rb") as file:
                # We need to read the whole file in binary for Parquet, while for the
                # others we just read 1KiB
                if format == "parquet":
                    data = file.read()
                else:
                    data = file.read(1024 * 1024)

            meta = await client.datasource_analyze_file(data)
    else:
        meta = connector.datasource_analyze(filename)
    return meta, data


async def _generate_datafile(
    filename: str, client: TinyB, format: str, connector: Optional[Connector] = None, force: Optional[bool] = False
):
    meta, data = await _analyze(filename, client, format, connector=connector)
    schema = meta["analysis"]["schema"]
    schema = schema.replace(", ", ",\n    ")
    datafile = f"""DESCRIPTION >\n    Generated from {filename}\n\nSCHEMA >\n    {schema}"""
    return generate_datafile(datafile, filename, data, force, _format=format)


async def folder_init(
    client: TinyB,
    folder: str,
    generate_datasources: Optional[bool] = False,
    force: Optional[bool] = False,
    generate_releases: Optional[bool] = False,
):
    for x in PROJECT_PATHS:
        try:
            f = Path(folder) / x
            f.mkdir()
            click.echo(FeedbackManager.info_path_created(path=x))
        except FileExistsError:
            if not force:
                click.echo(FeedbackManager.info_path_already_exists(path=x))
            pass

    if generate_datasources:
        for format in SUPPORTED_FORMATS:
            for path in Path(folder).glob(f"*.{format}"):
                await _generate_datafile(str(path), client, format=format, force=force)

    if generate_releases:
        base = Path(".")
        f = base / (".tinyenv")
        if not f.exists() or force:
            with open(".tinyenv", "w") as file:
                file.write("VERSION=0.0.0\n")
                click.echo(FeedbackManager.info_file_created(file=".tinyenv"))
        else:
            click.echo(FeedbackManager.info_dottinyenv_already_exists())

        base = Path("scripts")
        if not base.exists():
            base = Path()
        f = base / ("exec_test.sh")
        if not f.exists() or force:
            with open(f"{f}", "w") as t_file:
                t_file.write(
                    """
#!/usr/bin/env bash

fail=0;

for t in `find ./tests -name "*.test"`; do
  echo "** Running $t **"
  echo "** $(cat $t)"
  if res=$(bash $t $1 | diff -B ${t}.result -); then
    echo 'OK';
  else
    echo "failed, diff:";
    echo "$res";
    fail=1
  fi
  echo ""
done;

if [ $fail == 1 ]; then
  exit -1;
fi
"""
                )
            click.echo(FeedbackManager.info_file_created(file="scripts/exec_test.sh"))
        chmod(f, 0o755)

        base = Path("tests")
        if not base.exists():
            base = Path()
        f = base / ("example.yml")
        if not base.exists() or force:
            with open(f"{f}", "w") as t_file:
                t_file.write(
                    """
##########################################################################################################
###   Visit https://www.tinybird.co/docs/guides/implementing-test-strategies.html#data-quality-tests   ###
###   for more details on Data Quality tests                                                           ###
##########################################################################################################

- example_no_negative_numbers:
    max_bytes_read: null
    max_time: null
    sql: |
        SELECT
            number
        FROM numbers(10)
        WHERE
            number < 0

#    - example_top_products_params_no_empty_top_10_on_2023:
#       max_bytes_read: null
#       max_time: null
#       sql: |
#          SELECT *
#          FROM top_products_params
#          WHERE empty(top_10)
#       pipe:
#          name: top_products_params
#          params:
#             start: '2023-01-01'
#             end: '2023-12-31'

"""
                )


async def configure_connector(connector):
    if connector not in SUPPORTED_CONNECTORS:
        click.echo(FeedbackManager.error_invalid_connector(connectors=", ".join(SUPPORTED_CONNECTORS)))
        return

    file_name = f".tinyb_{connector}"
    config_file = Path(getcwd()) / file_name
    if connector == "bigquery":
        project = click.prompt("BigQuery project ID")
        service_account = click.prompt(
            "Path to a JSON service account file with permissions to export from BigQuery, write in Storage and sign URLs (leave empty to use GOOGLE_APPLICATION_CREDENTIALS environment variable)",
            default=environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""),
        )
        bucket_name = click.prompt("Name of a Google Cloud Storage bucket to store temporary exported files")

        try:
            config = {"project_id": project, "service_account": service_account, "bucket_name": bucket_name}
            await write_config(config, file_name)
        except Exception:
            raise CLIException(FeedbackManager.error_file_config(config_file=config_file))
    elif connector == "snowflake":
        sf_account = click.prompt("Snowflake Account (e.g. your-domain.west-europe.azure)")
        sf_warehouse = click.prompt("Snowflake warehouse name")
        sf_database = click.prompt("Snowflake database name")
        sf_schema = click.prompt("Snowflake schema name")
        sf_role = click.prompt("Snowflake role name")
        sf_user = click.prompt("Snowflake user name")
        sf_password = click.prompt("Snowflake password")
        sf_storage_integration = click.prompt(
            "Snowflake GCS storage integration name (leave empty to auto-generate one)", default=""
        )
        sf_stage = click.prompt("Snowflake GCS stage name (leave empty to auto-generate one)", default="")
        project = click.prompt("Google Cloud project ID to store temporary files")
        service_account = click.prompt(
            "Path to a JSON service account file with permissions to write in Storagem, sign URLs and IAM (leave empty to use GOOGLE_APPLICATION_CREDENTIALS environment variable)",
            default=environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""),
        )
        bucket_name = click.prompt("Name of a Google Cloud Storage bucket to store temporary exported files")

        if not service_account:
            service_account = getenv("GOOGLE_APPLICATION_CREDENTIALS")

        try:
            config = {
                "account": sf_account,
                "warehouse": sf_warehouse,
                "database": sf_database,
                "schema": sf_schema,
                "role": sf_role,
                "user": sf_user,
                "password": sf_password,
                "storage_integration": sf_storage_integration,
                "stage": sf_stage,
                "service_account": service_account,
                "bucket_name": bucket_name,
                "project_id": project,
            }
            await write_config(config, file_name)
        except Exception:
            raise CLIException(FeedbackManager.error_file_config(config_file=config_file))

        click.echo(FeedbackManager.success_connector_config(connector=connector, file_name=file_name))


async def _get_config(host, token, load_tb_file=True):
    config = {}

    try:
        client = TinyB(token, host, version=VERSION, send_telemetry=True)
        response = await client.workspace_info()
    except Exception:
        raise CLIAuthException(FeedbackManager.error_invalid_token_for_host(host=host))

    from_response = load_tb_file

    try:
        config_file = Path(getcwd()) / ".tinyb"
        with open(config_file) as file:
            config = json.loads(file.read())
    except Exception:
        from_response = True

    if not from_response:
        return config

    config.update({"host": host, "token": token, "id": response["id"], "name": response["name"]})

    if "user_email" in response:
        config["user_email"] = response["user_email"]
    if "user_id" in response:
        config["user_id"] = response["user_id"]
    if "scope" in response:
        config["scope"] = response["scope"]
    if "id" in response:
        config["id"] = response["id"]

    tokens = config.get("tokens", {})

    tokens.update({host: token})
    config["tokens"] = tokens
    config["token"] = tokens[host]
    config["host"] = host

    return config


async def get_regions(client: TinyB, config_file: Path) -> List[Dict[str, str]]:
    regions: List[Dict[str, str]] = []
    try:
        response = await client.regions()
        regions = response["regions"]
    except Exception:
        pass

    try:
        with open(config_file) as file:
            config = json.loads(file.read())
            if "tokens" not in config:
                return regions

            for key in config["tokens"]:
                region = next(
                    (region for region in regions if key == region["api_host"] or key == region["host"]), None
                )
                if region:
                    region["default_password"] = config["tokens"][key]
                else:
                    regions.append(
                        {
                            "api_host": format_host(key, subdomain="api"),
                            "host": format_host(key, subdomain="ui"),
                            "name": key,
                            "default_password": config["tokens"][key],
                        }
                    )

    except Exception:
        pass

    return regions


def _compare_hosts(region: Dict[str, Any], config: Dict[str, Any]) -> bool:
    return region["host"] == config["host"] or region["api_host"] == config["host"]


async def get_host_from_region(region_name_or_host_or_id: str, host: Optional[str] = None):
    is_localhost = FeatureFlags.is_localhost()

    if not host:
        host = DEFAULT_API_HOST if not is_localhost else DEFAULT_LOCALHOST

    client = _get_tb_client(token="", host=host)

    try:
        response = await client.regions()
        regions = response["regions"]
    except Exception:
        regions = []

    if not regions:
        click.echo(f"No regions available, using host: {host}")
        return [], host

    try:
        index = int(region_name_or_host_or_id)
        try:
            host = regions[index - 1]["api_host"]
        except Exception:
            raise CLIException(FeedbackManager.error_getting_region_by_index())
    except Exception:
        region_name_or_host_or_id = region_name_or_host_or_id.lower()
        try:
            region = next(
                (region for region in regions if _compare_region_host(region_name_or_host_or_id, region)), None
            )
            host = region["api_host"] if region else None
        except Exception:
            raise CLIException(FeedbackManager.error_getting_region_by_name_or_url())

    if not host:
        raise CLIException(FeedbackManager.error_getting_region_by_name_or_url())

    return regions, host


def _compare_region_host(region_name_or_host: str, region: Dict[str, Any]) -> bool:
    if region["name"].lower() == region_name_or_host:
        return True
    if region["host"] == region_name_or_host:
        return True
    if region["api_host"] == region_name_or_host:
        return True
    return False


def ask_for_region_interactively(regions):
    region_index = -1

    while region_index == -1:
        click.echo(FeedbackManager.info_available_regions())
        for index, region in enumerate(regions):
            click.echo(f"   [{index + 1}] {region['name'].lower()} ({region['host']})")
        click.echo("   [0] Cancel")

        region_index = click.prompt("\nUse region", default=1)

        if region_index == 0:
            click.echo(FeedbackManager.info_auth_cancelled_by_user())
            return None

        try:
            return regions[int(region_index) - 1]
        except Exception:
            available_options = ", ".join(map(str, range(1, len(regions) + 1)))
            click.echo(FeedbackManager.error_region_index(host_index=region_index, available_options=available_options))
            region_index = -1


def get_region_info(ctx, region=None):
    name = region["name"] if region else "default"
    api_host = format_host(
        region["api_host"] if region else ctx.obj["config"].get("host", DEFAULT_API_HOST), subdomain="api"
    )
    ui_host = format_host(region["host"] if region else ctx.obj["config"].get("host", DEFAULT_UI_HOST), subdomain="ui")
    return name, api_host, ui_host


def format_host(host: str, subdomain: Optional[str] = None) -> str:
    """
    >>> format_host('api.tinybird.co')
    'https://api.tinybird.co'
    >>> format_host('https://api.tinybird.co')
    'https://api.tinybird.co'
    >>> format_host('http://localhost:8001')
    'http://localhost:8001'
    >>> format_host('localhost:8001')
    'http://localhost:8001'
    >>> format_host('localhost:8001', subdomain='ui')
    'http://localhost:8001'
    >>> format_host('localhost:8001', subdomain='api')
    'http://localhost:8001'
    >>> format_host('https://api.tinybird.co', subdomain='ui')
    'https://ui.tinybird.co'
    >>> format_host('https://api.us-east.tinybird.co', subdomain='ui')
    'https://ui.us-east.tinybird.co'
    >>> format_host('https://api.us-east.tinybird.co', subdomain='api')
    'https://api.us-east.tinybird.co'
    >>> format_host('https://ui.us-east.tinybird.co', subdomain='api')
    'https://api.us-east.tinybird.co'
    >>> format_host('https://inditex-rt-pro.tinybird.co', subdomain='ui')
    'https://inditex-rt-pro.tinybird.co'
    >>> format_host('https://cluiente-tricky.tinybird.co', subdomain='api')
    'https://cluiente-tricky.tinybird.co'
    """
    is_localhost = FeatureFlags.is_localhost()
    if subdomain and not is_localhost:
        url_info = urlparse(host)
        current_subdomain = url_info.netloc.split(".")[0]
        if current_subdomain == "api" or current_subdomain == "ui":
            host = host.replace(current_subdomain, subdomain)
    if "localhost" in host or is_localhost:
        host = f"http://{host}" if "http" not in host else host
    elif not host.startswith("http"):
        host = f"https://{host}"
    return host


def region_from_host(region_name_or_host, regions):
    """Returns the region that matches region_name_or_host"""

    return next((r for r in regions if _compare_region_host(region_name_or_host, r)), None)


async def try_get_config(host, token):
    try:
        return await _get_config(host, token)
    except Exception:
        return None


async def authenticate(ctx, host, token=None, regions=None, interactive=False, try_all_regions=False):
    is_localhost = FeatureFlags.is_localhost()
    check_host = DEFAULT_API_HOST if not host and not is_localhost else DEFAULT_LOCALHOST

    client = _get_tb_client(token="", host=check_host)
    config_file = Path(getcwd()) / ".tinyb"
    default_password: Optional[str] = None

    if not regions and interactive:
        regions = await get_regions(client, config_file)

    selected_region = None

    if regions and interactive:
        selected_region = ask_for_region_interactively(regions)
        if selected_region is None:
            return None

        host = selected_region["api_host"]
        default_password = selected_region.get("default_password", None)
    elif regions and not interactive:
        selected_region = region_from_host(host, regions)

    if host and not regions and not selected_region:
        name, host, ui_host = (host, format_host(host, subdomain="api"), format_host(host, subdomain="ui"))
    else:
        name, host, ui_host = get_region_info(ctx, selected_region)

    token = token or ctx.ensure_object(dict)["config"].get("token_passed")

    if not token:
        tokens_url = urljoin(ui_host, "tokens")
        token = click.prompt(
            f"\nCopy the admin token from {tokens_url} and paste it here { f'OR press enter to use the token from .tinyb file' if default_password else ''}",
            hide_input=True,
            show_default=False,
            default=default_password,
        )

    add_telemetry_event("auth_token", token=token)

    config = await try_get_config(host, token)
    if config is None and not try_all_regions:
        raise CLIAuthException(FeedbackManager.error_invalid_token_for_host(host=host))

    # No luck? Let's try auth in all other regions
    if config is None and try_all_regions and not interactive:
        if not regions:
            regions = await get_regions(client, config_file)

        # Check other regions, ignoring the previously tested region
        for region in [r for r in regions if r is not selected_region]:
            name, host, ui_host = get_region_info(ctx, region)
            config = await try_get_config(host, token)
            if config is not None:
                click.echo(FeedbackManager.success_using_host(name=name, host=ui_host))
                break

    if config is None:
        raise CLIAuthException(FeedbackManager.error_invalid_token())

    try:
        if "id" in config:
            await write_config(config)
            ctx.ensure_object(dict)["client"] = _get_tb_client(config["token"], config.get("host", DEFAULT_API_HOST))
            ctx.ensure_object(dict)["config"] = config
        else:
            raise CLIAuthException(FeedbackManager.error_not_personal_auth())
    except Exception as e:
        raise CLIAuthException(FeedbackManager.error_exception(error=str(e)))

    click.echo(FeedbackManager.success_auth())
    click.echo(FeedbackManager.success_remember_api_host(api_host=host))

    if "scope" not in config or not config["scope"]:
        click.echo(FeedbackManager.warning_token_scope())

    if "scope" in config and config["scope"] == "admin":
        click.echo(FeedbackManager.warning_workspaces_admin_token())

    return config


def ask_for_user_token(action: str, ui_host: str) -> str:
    return click.prompt(
        f"\nIn order to {action} we need your user token. Copy it from {ui_host}/tokens and paste it here",
        hide_input=True,
        show_default=False,
        default=None,
    )


async def get_available_starterkits(ctx: Context) -> List[Dict[str, Any]]:
    ctx_dict = ctx.ensure_object(dict)
    available_starterkits = ctx_dict.get("available_starterkits", None)
    if available_starterkits is not None:
        return available_starterkits

    try:
        client: TinyB = ctx_dict["client"]

        available_starterkits = await client.starterkits()
        ctx_dict["available_starterkits"] = available_starterkits
        return available_starterkits
    except Exception as ex:
        click.echo(FeedbackManager.error_exception(error=ex))
        return []


async def get_starterkit(ctx: Context, name: str) -> Optional[Dict[str, Any]]:
    available_starterkits = await get_available_starterkits(ctx)
    if not available_starterkits:
        return None
    return next((sk for sk in available_starterkits if sk.get("friendly_name", None) == name), None)


async def is_valid_starterkit(ctx: Context, name: str) -> bool:
    return name == "blank" or (await get_starterkit(ctx, name) is not None)


async def ask_for_starterkit_interactively(ctx: Context) -> Optional[str]:
    starterkit = [{"friendly_name": "blank", "description": "Empty workspace"}]
    starterkit.extend(await get_available_starterkits(ctx))
    rows = [(index + 1, sk["friendly_name"], sk["description"]) for index, sk in enumerate(starterkit)]

    echo_safe_humanfriendly_tables_format_smart_table(rows, column_names=["Idx", "Id", "Description"])
    click.echo("")
    click.echo("   [0] to cancel")

    sk_index = -1
    while sk_index == -1:
        sk_index = click.prompt("\nUse starter kit", default=1)
        if sk_index < 0 or sk_index > len(starterkit):
            click.echo(FeedbackManager.error_starterkit_index(starterkit_index=sk_index))
            sk_index = -1

    if sk_index == 0:
        click.echo(FeedbackManager.info_cancelled_by_user())
        return None

    return starterkit[sk_index - 1]["friendly_name"]


async def fork_workspace(ctx: Context, client: TinyB, user_client: TinyB, created_workspace):
    config, _, _ = await get_config_and_hosts(ctx)

    datasources = await client.datasources()
    for datasource in datasources:
        await user_client.datasource_share(datasource["id"], config["id"], created_workspace["id"])


async def create_workspace_non_interactive(
    ctx: Context, workspace_name: str, starterkit: str, user_token: str, fork: bool
):
    """Creates a workspace using the provided name and starterkit"""
    client: TinyB = ctx.ensure_object(dict)["client"]

    try:
        user_client: TinyB = deepcopy(client)
        user_client.token = user_token

        created_workspace = await user_client.create_workspace(workspace_name, starterkit)
        click.echo(FeedbackManager.success_workspace_created(workspace_name=workspace_name))

        if fork:
            await fork_workspace(ctx, client, user_client, created_workspace)

    except Exception as e:
        raise CLIWorkspaceException(FeedbackManager.error_exception(error=str(e)))


async def create_workspace_interactive(
    ctx: Context, workspace_name: Optional[str], starterkit: Optional[str], user_token: str, fork: bool
):
    if not starterkit and not is_ci_environment():
        click.echo("\n")
        starterkit = await ask_for_starterkit_interactively(ctx)
        if not starterkit:  # Cancelled by user
            return

        if starterkit == "blank":  # 'blank' == empty workspace
            starterkit = None

    if not workspace_name:
        """Creates a workspace guiding the user"""
        click.echo("\n")
        click.echo(FeedbackManager.info_workspace_create_greeting())
        default_name = f"new_workspace_{uuid.uuid4().hex[0:4]}"
        workspace_name = click.prompt("\nWorkspace name", default=default_name, err=True, type=str)

    await create_workspace_non_interactive(ctx, workspace_name, starterkit, user_token, fork)  # type: ignore


async def create_workspace_branch(
    ctx: Context,
    branch_name: Optional[str],
    last_partition: Optional[bool],
    all: Optional[bool],
    ignore_datasources: Optional[List[str]],
    wait: Optional[bool],
) -> None:
    """
    Creates a workspace branch
    """
    client: TinyB = ctx.ensure_object(dict)["client"]

    try:
        config, _, _ = await get_config_and_hosts(ctx)
        workspace = await get_current_environment(client, config)

        if not workspace:
            raise CLIWorkspaceException(FeedbackManager.error_workspace())

        if not branch_name:
            click.echo(FeedbackManager.info_workspace_branch_create_greeting())
            default_name = f"{workspace['name']}_{uuid.uuid4().hex[0:4]}"
            branch_name = click.prompt("\Environment name", default=default_name, err=True, type=str)
        assert isinstance(branch_name, str)

        # Call the API wuth async=true to always spawn a job
        response = await client.create_workspace_branch(
            branch_name, last_partition, all, ignore_datasources, _async=True
        )
        assert isinstance(response, dict)

        is_job: bool = "job" in response
        is_summary: bool = "partitions" in response

        if not is_job and not is_summary:
            raise CLIException(str(response))

        if all and not is_job:
            raise CLIException(str(response))

        click.echo(
            FeedbackManager.success_workspace_branch_created(workspace_name=workspace["name"], branch_name=branch_name)
        )

        job_id: Optional[str] = None

        if is_job:
            job_id = response["job"]["job_id"]
            job_url = response["job"]["job_url"]
            click.echo(FeedbackManager.info_data_branch_job_url(url=job_url))

        if wait and is_job:
            assert isinstance(job_id, str)

            # Await the job to finish and get the result dict
            job_response = await wait_job(client, job_id, job_url, "Data Branching")
            if job_response is None:
                raise CLIException(f"Empty job API response (job_id: {job_id}, job_url: {job_url})")
            else:
                response = job_response.get("result", {})
                is_job = False
                is_summary = "partitions" in response

        await switch_workspace(ctx, branch_name, only_environments=True)
        if is_summary:
            await print_data_branch_summary(client, None, response)

    except Exception as e:
        raise CLIException(FeedbackManager.error_exception(error=str(e)))


async def print_data_branch_summary(client, job_id, response=None):
    response = await client.job(job_id) if job_id else response or {"partitions": []}
    columns = ["Data Source", "Partition", "Status", "Error"]
    table = []
    for partition in response["partitions"]:
        for p in partition["partitions"]:
            table.append([partition["datasource"]["name"], p["partition"], p["status"], p.get("error", "")])
    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)


async def print_branch_regression_tests_summary(client, job_id, host, response=None):
    def format_metric(metric: Union[str, float], is_percentage: bool = False) -> str:
        if isinstance(metric, float):
            if is_percentage:
                return f"{round(metric, 3):+} %"
            else:
                return f"{round(metric, 3)} seconds"
        else:
            return metric

    failed = False
    response = await client.job(job_id) if job_id else response or {"progress": []}
    output = "\n"
    for step in response["progress"]:
        run = step["run"]
        if run["output"]:
            output += "".join(run["output"])
        if not run["was_successfull"]:
            failed = True
    click.echo(output)

    if failed:
        click.echo("\n")
        click.echo("\n")
        click.echo("\n==== Failures Detail ====\n")
        click.echo("\n")
        for step in response["progress"]:
            if not step["run"]["was_successfull"]:
                for failure in step["run"]["failed"]:
                    try:
                        click.echo(f"❌ {failure['name']}")
                        click.echo(FeedbackManager.error_branch_check_pipe(error=failure["error"]))
                        click.echo("\n")
                    except Exception:
                        pass

    click.echo("\n")
    click.echo("\n")
    click.echo("\n==== Performance metrics ====\n")
    click.echo("\n")
    for step in response["progress"]:
        run = step["run"]
        if run.get("metrics_summary") and run.get("metrics_timing"):
            column_names = [f"{run['pipe_name']}({run['test_type']})", "Origin", "Environment", "Delta"]

            click.echo(
                format_pretty_table(
                    [
                        [
                            metric,
                            format_metric(run["metrics_timing"][metric][0]),
                            format_metric(run["metrics_timing"][metric][1]),
                            format_metric(run["metrics_timing"][metric][2], is_percentage=True),
                        ]
                        for metric in [
                            "min response time",
                            "max response time",
                            "mean response time",
                            "median response time",
                            "p90 response time",
                            "min read bytes",
                            "max read bytes",
                            "mean read bytes",
                            "median read bytes",
                            "p90 read bytes",
                        ]
                    ],
                    column_names=column_names,
                )
            )

    click.echo("\n")
    click.echo("\n")
    click.echo("\n==== Results Summary ====\n")
    click.echo("\n")
    click.echo(
        format_pretty_table(
            [
                [
                    step["run"]["pipe_name"],
                    step["run"]["test_type"],
                    step["run"]["metrics_summary"].get("run", 0),
                    step["run"]["metrics_summary"].get("passed", 0),
                    step["run"]["metrics_summary"].get("failed", 0),
                    format_metric(
                        step["run"]["metrics_timing"]["mean response time"][2]
                        if "mean response time" in step["run"]["metrics_timing"]
                        else 0.0,
                        is_percentage=True,
                    ),
                    format_metric(
                        step["run"]["metrics_timing"]["mean read bytes"][2]
                        if "mean read bytes" in step["run"]["metrics_timing"]
                        else 0.0,
                        is_percentage=True,
                    ),
                ]
                for step in response["progress"]
            ],
            column_names=["Endpoint", "Test", "Run", "Passed", "Failed", "Mean response time", "Mean read bytes"],
        )
    )
    if failed:
        for step in response["progress"]:
            if not step["run"]["was_successfull"]:
                for failure in step["run"]["failed"]:
                    click.echo(f"❌ FAILED {failure['name']}\n")
    if failed:
        raise click.ClickException(
            "Check Failures Detail above for more information. If the results are expected, skip asserts or increase thresholds, see 💡 Hints above (note skip asserts flags are applied to all regression tests, so use them when it makes sense).\n\nIf you are using the CI template for GitHub or GitLab you can add skip asserts flags as labels to the MR and they are automatically applied. Find available flags to skip asserts and thresholds here => https://www.tinybird.co/docs/guides/continuous-integration.html#run-the-tests"
        )


async def deploy_environment(
    ctx: Context,
    branch_id: str,
    current_main_workspace: Any,
    wait: Optional[bool],
    verbose: Optional[bool],
    commit: str,
    semver: str,
    data_migrations: Any,
    dry_run: bool,
):
    """
    Merges a workspace branch
    """
    client: TinyB = ctx.ensure_object(dict)["client"]

    try:
        config, _, _ = await get_config_and_hosts(ctx)
        response = await client.deploy_environment(
            branch_id, semver, commit, data_migrations=data_migrations, dry_run=dry_run
        )

        await switch_workspace(ctx, current_main_workspace["name"])
        client = ctx.ensure_object(dict)["client"]

        if wait and not dry_run:
            job_id = response["job"]["job_id"]
            job_url = response["job"]["job_url"]
            click.echo(FeedbackManager.info_merge_branch_job_url(url=job_url))
            merge_branch_status = MergeBranchStatus(verbose)
            await wait_job(
                client,
                job_id,
                job_url,
                "Environment Deployment",
                wait_observer=partial(merge_branch_status.print_merge_branch_summary),
            )
        elif dry_run:
            merge_branch_status = MergeBranchStatus(verbose)
            merge_branch_status.print_merge_branch_summary(response)
            click.secho(" ** DATA MIGRATIONS:")
            click.secho(json.dumps({"data_migrations": response["data_migrations"]}, indent=4))
            click.secho(
                "You can save the above JSON to a file, modify it and run it with `tb env deploy --migrations <file> --wait --semver <semver>`"
            )
            await switch_workspace(ctx, config["name"], only_environments=True)
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        await switch_workspace(ctx, config["name"], only_environments=True)


class MergeBranchStatus:
    def __init__(self, verbose=False):
        self.last_step = 0
        self.verbose = verbose

    def print_merge_branch_summary(self, response=None, progress_bar=None):
        if not response:
            return
        step = 0
        for part in response["progress"]:
            try:
                step = int(part["step"])
                timestamp = part["timestamp"]
                if step > self.last_step:
                    self.last_step = step
                    if part["verbose"] is True and not self.verbose:
                        continue
                    if step == 1:
                        click.echo("\n\n")
                    elif part["message"].startswith("====="):
                        click.echo(part["message"])
                        continue
                    elif part["message"] == "":
                        click.echo("\n")
                        continue

                    click.echo(f"{timestamp} => {part['message']}")
            except Exception:
                pass
        self.last_step = step


class PlanName(Enum):
    DEV = "Build"
    PRO = "Pro"
    ENTERPRISE = "Enterprise"


def _get_workspace_plan_name(plan):
    if plan == "dev":
        return PlanName.DEV.value
    if plan == "pro":
        return PlanName.PRO.value
    if plan == "enterprise":
        return PlanName.ENTERPRISE.value
    return "Custom"


def get_format_from_filename_or_url(filename_or_url: str) -> str:
    """
    >>> get_format_from_filename_or_url('wadus_parquet.csv')
    'csv'
    >>> get_format_from_filename_or_url('wadus_csv.parquet')
    'parquet'
    >>> get_format_from_filename_or_url('wadus_csv.ndjson')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_csv.json')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_parquet.csv?auth=pepe')
    'csv'
    >>> get_format_from_filename_or_url('wadus_csv.parquet?auth=pepe')
    'parquet'
    >>> get_format_from_filename_or_url('wadus_parquet.ndjson?auth=pepe')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus.json?auth=pepe')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_csv_')
    'csv'
    >>> get_format_from_filename_or_url('wadus_json_csv_')
    'csv'
    >>> get_format_from_filename_or_url('wadus_json_')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_ndjson_')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_parquet_')
    'parquet'
    >>> get_format_from_filename_or_url('wadus')
    'csv'
    >>> get_format_from_filename_or_url('https://storage.googleapis.com/tinybird-waduscom/stores_stock__v2_1646741850424_final.csv?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=44444444444-compute@developer.gserviceaccount.com/1234/auto/storage/goog4_request&X-Goog-Date=20220308T121750Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=8888888888888888888888888888888888888888888888888888888')
    'csv'
    """
    filename_or_url = filename_or_url.lower()
    if filename_or_url.endswith("json") or filename_or_url.endswith("ndjson"):
        return "ndjson"
    if filename_or_url.endswith("parquet"):
        return "parquet"
    if filename_or_url.endswith("csv"):
        return "csv"
    try:
        parsed = urlparse(filename_or_url)
        if parsed.path.endswith("json") or parsed.path.endswith("ndjson"):
            return "ndjson"
        if parsed.path.endswith("parquet"):
            return "parquet"
        if parsed.path.endswith("csv"):
            return "csv"
    except Exception:
        pass
    if "csv" in filename_or_url:
        return "csv"
    if "json" in filename_or_url:
        return "ndjson"
    if "parquet" in filename_or_url:
        return "parquet"
    return "csv"


async def push_data(
    ctx,
    datasource_name,
    url,
    connector,
    sql,
    mode="append",
    sql_condition=None,
    replace_options=None,
    ignore_empty=False,
    concurrency=1,
):
    if url and type(url) is tuple:
        url = url[0]
    client = ctx.obj["client"]

    if connector:
        load_connector_config(ctx, connector, False, check_uninstalled=False)
        if connector not in ctx.obj:
            click.echo(FeedbackManager.error_connector_not_configured(connector=connector))
            return
        else:
            _connector = ctx.obj[connector]
            click.echo(FeedbackManager.info_starting_export_process(connector=connector))
            try:
                url = _connector.export_to_gcs(sql, datasource_name, mode)
            except ConnectorNothingToLoad as e:
                if ignore_empty:
                    click.echo(str(e))
                    return
                else:
                    raise e

    def cb(res):
        if cb.First:
            blocks_to_process = len([x for x in res["block_log"] if x["status"] == "idle"])
            if blocks_to_process:
                cb.bar = click.progressbar(label=FeedbackManager.info_progress_blocks(), length=blocks_to_process)
                cb.bar.update(0)
                cb.First = False
                cb.blocks_to_process = blocks_to_process
        else:
            done = len([x for x in res["block_log"] if x["status"] == "done"])
            if done * 2 > cb.blocks_to_process:
                cb.bar.label = FeedbackManager.info_progress_current_blocks()
            cb.bar.update(done - cb.prev_done)
            cb.prev_done = done

    cb.First = True
    cb.prev_done = 0

    click.echo(FeedbackManager.info_starting_import_process())

    if isinstance(url, list):
        urls = url
    else:
        urls = [url]

    async def process_url(datasource_name, url, mode, sql_condition, replace_options):
        parsed = urlparse(url)
        # poor man's format detection
        _format = get_format_from_filename_or_url(url)
        if parsed.scheme in ("http", "https"):
            res = await client.datasource_create_from_url(
                datasource_name,
                url,
                mode=mode,
                status_callback=cb,
                sql_condition=sql_condition,
                format=_format,
                replace_options=replace_options,
            )
        else:
            res = await client.datasource_append_data(
                datasource_name,
                file=url,
                mode=mode,
                sql_condition=sql_condition,
                format=_format,
                replace_options=replace_options,
            )

        datasource_name = res["datasource"]["name"]
        try:
            datasource = await client.get_datasource(datasource_name)
        except DoesNotExistException:
            click.echo(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
        except Exception as e:
            click.echo(FeedbackManager.error_exception(error=str(e)))
            return

        total_rows = (datasource.get("statistics", {}) or {}).get("row_count", 0)
        appended_rows = 0
        parser = None

        if "error" in res and res["error"]:
            click.echo(FeedbackManager.error_exception(error=res["error"]))
        if "errors" in res and res["errors"]:
            click.echo(FeedbackManager.error_exception(error=res["errors"]))
        if "blocks" in res and res["blocks"]:
            for block in res["blocks"]:
                if "process_return" in block and block["process_return"] is not None:
                    process_return = block["process_return"][0]
                    parser = (
                        process_return["parser"] if "parser" in process_return and process_return["parser"] else parser
                    )
                    if parser and parser != "clickhouse":
                        parser = process_return["parser"]
                        appended_rows += process_return["lines"]

        return parser, total_rows, appended_rows

    async def gather_with_concurrency(n, *tasks):
        semaphore = asyncio.Semaphore(n)

        async def sem_task(task):
            async with semaphore:
                return await task

        return await asyncio.gather(*(sem_task(task) for task in tasks))

    try:
        tasks = [process_url(datasource_name, url, mode, sql_condition, replace_options) for url in urls]
        output = await gather_with_concurrency(concurrency, *tasks)
        parser, total_rows, appended_rows = list(output)[-1]
    except OperationCanNotBePerformed as e:
        click.echo(FeedbackManager.error_operation_can_not_be_performed(error=e))
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=e))
        sys.exit(1)
    else:
        click.echo(FeedbackManager.success_progress_blocks())
        if mode == "append":
            if parser != "clickhouse":
                click.echo(FeedbackManager.success_appended_rows(appended_rows=appended_rows))

        click.echo(FeedbackManager.success_total_rows(datasource=datasource_name, total_rows=total_rows))

        if mode == "replace":
            click.echo(FeedbackManager.success_replaced_datasource(datasource=datasource_name))
        else:
            click.echo(FeedbackManager.success_appended_datasource(datasource=datasource_name))
        click.echo(FeedbackManager.info_data_pushed(datasource=datasource_name))
    finally:
        try:
            for url in urls:
                _connector.clean(urlparse(url).path.split("/")[-1])
        except Exception:
            pass


async def sync_data(ctx, datasource_name: str):
    client: TinyB = ctx.obj["client"]
    datasource = await client.get_datasource(datasource_name)
    VALID_DATASOURCES = ["bigquery", "snowflake", "s3"]
    if datasource["type"] not in VALID_DATASOURCES:
        raise CLIException(FeedbackManager.error_sync_not_supported(valid_datasources=VALID_DATASOURCES))
    await client.datasource_sync(datasource["id"])


# eval "$(_TB_COMPLETE=source_bash tb)"
def autocomplete_topics(ctx: Context, args, incomplete):
    try:
        config = async_to_sync(get_config)(None, None)
        ctx.ensure_object(dict)["config"] = config
        client = create_tb_client(ctx)
        topics = async_to_sync(client.kafka_list_topics)(args[2])
        return [t for t in topics if incomplete in t]
    except Exception:
        return []


def validate_datasource_name(name):
    if not isinstance(name, str) or str == "":
        raise CLIException(FeedbackManager.error_datasource_name())


def validate_connection_id(connection_id):
    if not isinstance(connection_id, str) or str == "":
        raise CLIException(FeedbackManager.error_datasource_connection_id())


def validate_kafka_topic(topic):
    if not isinstance(topic, str):
        raise CLIException(FeedbackManager.error_kafka_topic())


def validate_kafka_group(group):
    if not isinstance(group, str):
        raise CLIException(FeedbackManager.error_kafka_group())


def validate_kafka_auto_offset_reset(auto_offset_reset):
    valid_values = {"latest", "earliest", "none"}
    if not (auto_offset_reset in valid_values):
        raise CLIException(FeedbackManager.error_kafka_auto_offset_reset())


def validate_kafka_schema_registry_url(schema_registry_url):
    if not is_url_valid(schema_registry_url):
        raise CLIException(FeedbackManager.error_kafka_registry())


def is_url_valid(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_kafka_bootstrap_servers(host_and_port):
    if not isinstance(host_and_port, str):
        raise CLIException(FeedbackManager.error_kafka_bootstrap_server())
    parts = host_and_port.split(":")
    if len(parts) > 2:
        raise CLIException(FeedbackManager.error_kafka_bootstrap_server())
    host = parts[0]
    port = parts[1] if len(parts) == 2 else "9092"
    try:
        port = int(port)
    except Exception:
        raise CLIException(FeedbackManager.error_kafka_bootstrap_server())
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        try:
            sock.settimeout(3)
            sock.connect((host, port))
        except socket.timeout:
            raise CLIException(FeedbackManager.error_kafka_bootstrap_server_conn_timeout())
        except Exception:
            raise CLIException(FeedbackManager.error_kafka_bootstrap_server_conn())


def validate_kafka_key(s):
    if not isinstance(s, str):
        raise CLIException("Key format is not correct, it should be a string")


def validate_kafka_secret(s):
    if not isinstance(s, str):
        raise CLIException("Password format is not correct, it should be a string")


def validate_string_connector_param(param, s):
    if not isinstance(s, str):
        raise CLIConnectionException(param + " format is not correct, it should be a string")


async def validate_connection_name(client, connection_name, service):
    if await client.get_connector(connection_name, service) is not None:
        raise CLIConnectionException(FeedbackManager.error_connection_already_exists(name=connection_name))


def _get_setting_value(connection, setting, sensitive_settings):
    if setting in sensitive_settings:
        return "*****"
    return connection.get(setting, "")


async def _get_config_or_load_tb_file(config):
    if "id" not in config:
        config = await _get_config(config["host"], config["token"], load_tb_file=False)
    else:
        config_file = Path(getcwd()) / ".tinyb"
        with open(config_file) as file:
            config = json.loads(file.read())
    return config


async def switch_workspace(ctx, workspace_name_or_id, only_environments=False):
    client: TinyB = ctx.ensure_object(dict)["client"]
    config = ctx.ensure_object(dict)["config"]

    try:
        config = await _get_config(config["host"], config["token"], load_tb_file=False)

        if only_environments:
            workspaces = await get_current_workspace_branches(client, config)
        else:
            response = await client.user_workspaces()
            workspaces = response["workspaces"]

        workspace = next(
            (
                workspace
                for workspace in workspaces
                if workspace["name"] == workspace_name_or_id or workspace["id"] == workspace_name_or_id
            ),
            None,
        )

        if not workspace:
            if only_environments:
                click.echo(FeedbackManager.error_branch(branch=workspace_name_or_id))
            else:
                click.echo(FeedbackManager.error_workspace(workspace=workspace_name_or_id))
            return

        client = _get_tb_client(workspace["token"], config["host"])

        config["id"] = workspace["id"]
        config["name"] = workspace["name"]
        config["token"] = workspace["token"]
        host = config["host"]

        tokens = config.get("tokens", {})
        tokens[host] = config["token"]

        config["tokens"] = tokens

        ctx.ensure_object(dict)["client"] = client
        ctx.ensure_object(dict)["config"] = config

        await write_config(config)
        click.echo(FeedbackManager.success_now_using_config(name=config["name"], id=config["id"]))
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return


async def switch_to_workspace_by_user_workspace_data(ctx, user_workspace_data: Dict):
    config = ctx.ensure_object(dict)["config"]

    try:
        config = await _get_config_or_load_tb_file(config)

        client = TinyB(user_workspace_data["token"], config["host"], version=VERSION, send_telemetry=True)

        config["id"] = user_workspace_data["id"]
        config["name"] = user_workspace_data["name"]
        config["token"] = user_workspace_data["token"]
        host = config["host"]

        tokens = config.get("tokens", {})
        tokens[host] = config["token"]

        config["tokens"] = tokens

        ctx.ensure_object(dict)["client"] = client
        ctx.ensure_object(dict)["config"] = config

        await write_config(config)
        click.echo(FeedbackManager.success_now_using_config(name=config["name"], id=config["id"]))
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return


async def print_current_workspace(ctx):
    client: TinyB = ctx.ensure_object(dict)["client"]
    config = ctx.ensure_object(dict)["config"]

    if "id" not in config:
        config = await _get_config(config["host"], config["token"], load_tb_file=False)

    current_main_workspace = await get_current_main_workspace(client, config)

    columns = ["name", "id", "role", "plan", "current"]

    table = [
        (
            current_main_workspace["name"],
            current_main_workspace["id"],
            current_main_workspace["role"],
            _get_workspace_plan_name(current_main_workspace["plan"]),
            True,
        )
    ]

    click.echo(FeedbackManager.info_current_workspace())
    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)


async def print_current_branch(ctx):
    client: TinyB = ctx.ensure_object(dict)["client"]
    config = ctx.ensure_object(dict)["config"]

    if "id" not in config:
        config = await _get_config(config["host"], config["token"], load_tb_file=False)

    response = await client.user_workspaces_and_branches()

    columns = ["name", "id", "main"]
    table = []

    for workspace in response["workspaces"]:
        if config["id"] == workspace["id"]:
            click.echo(FeedbackManager.info_current_branch())
            if workspace.get("is_branch"):
                name = workspace["name"]
                main_workspace = await get_current_main_workspace(client, config)
                main_name = main_workspace["name"]
            else:
                name = MAIN_BRANCH
                main_name = workspace["name"]
            table.append([name, workspace["id"], main_name])
            break

    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)


class ConnectionReplacements:
    _PARAMS_REPLACEMENTS: Dict[str, Dict[str, str]] = {
        "s3": {
            "service": "service",
            "connection_name": "name",
            "key": "s3_access_key_id",
            "secret": "s3_secret_access_key",
            "region": "s3_region",
        },
        "gcs_hmac": {
            "service": "service",
            "connection_name": "name",
            "key": "gcs_hmac_access_id",
            "secret": "gcs_hmac_secret",
            "region": "gcs_region",
        },
    }

    @staticmethod
    def map_api_params_from_prompt_params(service: str, **params: Any) -> Dict[str, Any]:
        """Maps prompt parameters to API parameters."""

        api_params = {}
        for key in params.keys():
            try:
                api_params[ConnectionReplacements._PARAMS_REPLACEMENTS[service][key]] = params[key]
            except KeyError:
                api_params[key] = params[key]

        api_params["service"] = service
        return api_params
