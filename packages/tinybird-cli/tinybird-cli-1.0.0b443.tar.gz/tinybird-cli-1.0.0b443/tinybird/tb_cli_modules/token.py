import click
import pyperclip

from click import Context
from typing import Any, Dict, Optional

from tinybird.feedback_manager import FeedbackManager
from tinybird.client import TinyB
from tinybird.tb_cli_modules.common import (
    coro,
    echo_safe_humanfriendly_tables_format_smart_table,
    DoesNotExistException,
)
from tinybird.tb_cli_modules.cli import cli
from tinybird.tb_cli_modules.exceptions import CLITokenException


@cli.group(hidden=True)
@click.pass_context
def token(ctx: Context) -> None:
    """Token commands."""


@token.command(name="ls")
@click.option("--match", default=None, help="Retrieve any token matching the pattern. eg --match _test")
@click.pass_context
@coro
async def token_ls(
    ctx: Context,
    match: Optional[str] = None,
) -> None:
    """List tokens."""

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]

    try:
        tokens = await client.token_list(match)
        columns = ["id", "name", "description"]
        table = list(map(lambda token: [token.get(key, "") for key in columns], tokens))

        click.echo(FeedbackManager.info_tokens())
        echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)
        click.echo("\n")
    except Exception as e:
        raise CLITokenException(FeedbackManager.error_exception(error=e))


@token.command(name="rm")
@click.argument("token_id")
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
@click.pass_context
@coro
async def token_rm(ctx: Context, token_id: str, yes: bool) -> None:
    """Remove a token."""

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]
    if yes or click.confirm(FeedbackManager.warning_confirm_delete_token(token=token_id)):
        try:
            await client.token_delete(token_id)
        except DoesNotExistException:
            raise CLITokenException(FeedbackManager.error_token_does_not_exist(token_id=token_id))
        except Exception as e:
            raise CLITokenException(FeedbackManager.error_exception(error=e))
        click.echo(FeedbackManager.success_delete_token(token=token_id))


@token.command(name="refresh")
@click.argument("token_id")
@click.pass_context
@coro
async def token_refresh(ctx: Context, token_id: str) -> None:
    """Refresh a token."""

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]

    try:
        await client.token_refresh(token_id)
    except DoesNotExistException:
        raise CLITokenException(FeedbackManager.error_token_does_not_exist(token=token_id))
    except Exception as e:
        raise CLITokenException(FeedbackManager.error_exception(error=e))
    click.echo(FeedbackManager.success_refresh_token(token=token_id))


@token.command(name="scopes")
@click.argument("token_id")
@click.pass_context
@coro
async def token_scopes(ctx: Context, token_id: str) -> None:
    """List token scopes."""

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]

    try:
        scopes = await client.token_scopes(token_id)
        columns = ["type", "resource", "filter"]
        table = list(map(lambda scope: [scope.get(key, "") for key in columns], scopes))
        click.echo(FeedbackManager.info_token_scopes(token=token_id))
        echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)
        click.echo("\n")
    except Exception as e:
        raise CLITokenException(FeedbackManager.error_exception(error=e))


@token.command(name="copy")
@click.argument("token_id")
@click.pass_context
@coro
async def token_copy(ctx: Context, token_id: str) -> None:
    """Copy a token."""

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]

    try:
        token = await client.token_get(token_id)
        pyperclip.copy(token["token"].strip())
    except DoesNotExistException:
        raise CLITokenException(FeedbackManager.error_token_does_not_exist(token=token_id))
    except Exception as e:
        raise CLITokenException(FeedbackManager.error_exception(error=e))
    click.echo(FeedbackManager.success_copy_token(token=token_id))
