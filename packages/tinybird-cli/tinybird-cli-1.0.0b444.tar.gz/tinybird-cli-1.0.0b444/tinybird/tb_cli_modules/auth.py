# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import json
import click

from os import getcwd, getenv
from pathlib import Path
from click import Context
from urllib.parse import urlparse
from typing import Any, Dict, Optional

from tinybird.client import TinyB
from tinybird.feedback_manager import FeedbackManager
from tinybird.config import DEFAULT_API_HOST, DEFAULT_LOCALHOST, VERSION, FeatureFlags, write_config

from tinybird.tb_cli_modules.cli import cli
from tinybird.tb_cli_modules.common import (
    _compare_hosts,
    _get_config,
    authenticate,
    configure_connector,
    coro,
    get_host_from_region,
    get_regions,
    echo_safe_humanfriendly_tables_format_smart_table,
)
from tinybird.tb_cli_modules.exceptions import CLIAuthException
from tinybird.tb_cli_modules.telemetry import add_telemetry_event


@cli.group(invoke_without_command=True)
@click.option("--token", envvar="TB_TOKEN", help="Use auth token, defaults to TB_TOKEN envvar, then to the .tinyb file")
@click.option(
    "--host",
    envvar="TB_HOST",
    help="Set custom host if it's different than https://api.tinybird.co. Check https://docs.tinybird.co/cli.html for the available list of regions",
)
@click.option("--region", envvar="TB_REGION", help="Set region. Run 'tb auth ls' to show available regions")
@click.option(
    "--connector",
    type=click.Choice(["bigquery", "snowflake"], case_sensitive=True),
    help="Set credentials for one of the supported connectors",
)
@click.option(
    "-i",
    "--interactive",
    is_flag=True,
    default=False,
    help="Show available regions and select where to authenticate to",
)
@click.pass_context
@coro
async def auth(ctx: Context, token: str, host: str, region: str, connector: str, interactive: bool) -> None:
    """Configure auth."""

    if connector:
        await configure_connector(connector)
        return

    if host:
        # Let's keep just the basic url
        url_info = urlparse(host)
        host = f"{url_info.scheme}://{url_info.netloc}"

    # only run when doing 'tb auth'
    if not ctx.invoked_subcommand:
        regions = None

        if region:
            regions, host = await get_host_from_region(region, host)

        config = None

        try:
            config = await authenticate(
                ctx, host=host, token=token, regions=regions, interactive=interactive, try_all_regions=True
            )
            add_telemetry_event("auth_success")
        except Exception as e:
            msg = FeedbackManager.error_exception(error=str(e))
            raise CLIAuthException(msg)

        if not config:
            msg = FeedbackManager.error_auth()
            raise CLIAuthException(msg)

    elif ctx.invoked_subcommand == "ls":
        pass

    else:
        config = None
        try:
            config_file = Path(getcwd()) / ".tinyb"
            with open(config_file) as file:
                config = json.loads(file.read())
            ctx.ensure_object(dict)["client"] = TinyB(
                config["token"], config.get("host", DEFAULT_API_HOST), version=VERSION, send_telemetry=True
            )
            ctx.ensure_object(dict)["config"] = config
        except Exception:
            host = ctx.ensure_object(dict)["config"].get("host", DEFAULT_API_HOST)
            token = ctx.ensure_object(dict)["config"]["token"]

            if not token:
                raise CLIAuthException(FeedbackManager.error_notoken())

            config = await _get_config(host, token)
            ctx.ensure_object(dict)["config"] = config

        if not config or not config["token"]:
            msg = FeedbackManager.error_wrong_config_file(config_file=config_file)
            raise CLIAuthException(msg)


@auth.command(name="info")
@click.pass_context
@coro
async def auth_info(ctx: Context):
    """Get information about the authentication that is currently being used"""
    config = ctx.ensure_object(dict)["config"]

    if config and "id" in config:
        columns = ["user", "token", "host", "workspace_name", "workspace_id"]
        table = []
        user_email = config["user_email"] if "user_email" in config else "No user"

        def value_or_none(value: Optional[str], pattern: str) -> Optional[str]:
            if not value:
                return None
            return pattern.format(value)

        def obfuscate(value: Optional[str]) -> Optional[str]:
            if not value:
                return None
            return f"{value[:4]}...{value[-8:]}"

        token = value_or_none(obfuscate(getenv("TB_TOKEN")), "{0} ($TB_TOKEN)")
        if not token:
            token = value_or_none(obfuscate(config.get("token")), "{0} (.tinyb)")

        host = value_or_none(getenv("TB_HOST", None), "{0} ($TB_HOST)")
        if not host:
            host = value_or_none(config.get("host", None), "{0} (.tinyb)")

        table.append([user_email, token, host, config["name"], config["id"]])
        echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)


@auth.command(name="ls")
@click.pass_context
@coro
async def auth_ls(ctx: Context) -> None:
    """List available regions to authenticate."""

    config = ctx.ensure_object(dict)["config"]

    config_file = Path(getcwd()) / ".tinyb"
    is_localhost = FeatureFlags.is_localhost()
    check_host = config.get("host", DEFAULT_API_HOST)
    check_host = check_host if not is_localhost else DEFAULT_LOCALHOST
    client = TinyB(token="", host=check_host, version=VERSION, send_telemetry=True)

    columns = ["idx", "region", "host", "api", "current"]
    table = []
    click.echo(FeedbackManager.info_available_regions())

    regions = await get_regions(client, config_file)

    if regions:
        for index, region in enumerate(regions):
            table.append(
                [index + 1, region["name"].lower(), region["host"], region["api_host"], _compare_hosts(region, config)]
            )
    else:
        table.append([1, "default", config["host"], True])

    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)


@auth.command(name="use")
@click.argument("region_name_or_host_or_id")
@click.pass_context
@coro
async def auth_use(ctx: Context, region_name_or_host_or_id: str) -> None:
    """Switch to a different region.
    You can pass the region name, the region host url, or the region index
    after listing available regions with 'tb auth ls'

    \b
    Example usage:
    \b
    $ tb auth use us-east
    $ tb auth use 1
    $ tb auth use https://ui.us-east.tinybird.co
    """

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    config: Dict[str, Any] = obj["config"]

    token: Optional[str] = None
    host = config.get("host", None)

    regions, host = await get_host_from_region(region_name_or_host_or_id, host)

    if "tokens" in config and host in config["tokens"]:
        token = config["tokens"][host]

    config = await authenticate(ctx, host, token, regions)

    await write_config(config)
    click.echo(FeedbackManager.success_now_using_config(name=config["name"], id=config["id"]))
