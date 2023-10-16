# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

from typing import Any, Dict, List, Tuple, Optional
import click
from click import Context
import yaml
import json

from tinybird.client import TinyB
from tinybird.tb_cli_modules.cli import cli
from tinybird.tb_cli_modules.common import (
    coro,
    get_config_and_hosts,
    create_workspace_branch,
    switch_workspace,
    switch_to_workspace_by_user_workspace_data,
    print_current_workspace,
    _get_config,
    print_data_branch_summary,
    echo_safe_humanfriendly_tables_format_smart_table,
    get_current_main_workspace,
    get_current_workspace_branches,
    MAIN_BRANCH,
    print_current_branch,
    print_branch_regression_tests_summary,
    deploy_environment,
)
from tinybird.feedback_manager import FeedbackManager
from tinybird.datafile import wait_job, CLIGitRelease, CLIGitReleaseException
from tinybird.config import VERSION
from tinybird.tb_cli_modules.exceptions import CLIBranchException, CLIReleaseException


@cli.group(hidden=True)
@click.pass_context
def release(ctx: Context) -> None:
    """Release commands"""


@release.command(name="ls", short_help="Lists Releases for the current Workspace")
@click.pass_context
@coro
async def release_ls(ctx: Context) -> None:
    """List current available Releases in the Workspace"""

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]
    config = obj["config"]

    if "id" not in config:
        config = await _get_config(config["host"], config["token"], load_tb_file=False)

    response = await client.releases(config["id"])

    columns = ["created_at", "semver", "status", "commit", "rollback release"]
    table: List[Tuple[str, str, str, str, str]] = []

    for release in response["releases"]:
        table.append(
            (release["created_at"], release["semver"], release["status"], release["commit"], release["rollback"])
        )

    click.echo(FeedbackManager.info_releases())
    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)


@release.command(name="promote", short_help="Promotes to live status a preview Release")
@click.option(
    "--semver",
    is_flag=False,
    required=True,
    type=str,
    help="Semver of a preview Release to promote to live. Example: 1.0.0",
)
@click.pass_context
@coro
async def release_promote(ctx: Context, semver: str) -> None:
    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]
    config = obj["config"]

    if "id" not in config:
        config = await _get_config(config["host"], config["token"], load_tb_file=False)

    current_main_workspace = await get_current_main_workspace(client, config)
    # FIXME validate is not environment

    if current_main_workspace["id"] != config["id"]:
        client = TinyB(current_main_workspace["token"], config["host"], version=VERSION, send_telemetry=True)

    try:
        await client.release_promote(current_main_workspace["id"], semver)
        click.echo(FeedbackManager.success_release_promote(semver=semver))
    except Exception as e:
        raise CLIReleaseException(FeedbackManager.error_exception(error=str(e)))


@release.command(name="rollback", short_help="Rollbacks to a previous Release")
@click.pass_context
@coro
async def release_rollback(ctx: Context) -> None:
    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]
    config = obj["config"]

    if "id" not in config:
        config = await _get_config(config["host"], config["token"], load_tb_file=False)

    current_main_workspace = await get_current_main_workspace(client, config)

    if current_main_workspace["id"] != config["id"]:
        client = TinyB(current_main_workspace["token"], config["host"], version=VERSION, send_telemetry=True)

    # FIXME validate current_main_workspace has a release with semver
    try:
        release = await client.release_rollback(
            current_main_workspace["id"], semver=current_main_workspace["release"]["semver"]
        )
        click.echo(FeedbackManager.success_release_rollback(semver=release["semver"]))
    except Exception as e:
        raise CLIReleaseException(FeedbackManager.error_exception(error=str(e)))


@release.command(name="rm", short_help="Removes a preview or failed Release. This action is irreversible")
@click.option(
    "--semver",
    is_flag=False,
    required=True,
    type=str,
    help="Semver of a preview or failed Release to delete. Example: 1.0.0",
)
@click.option(
    "--force", is_flag=True, default=False, help="USE WITH CAUTION! Allows to delete a Release that is currently in use"
)
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
@click.option(
    "--dry-run", is_flag=True, default=False, help="Checks the Release could be deleted without actually deleting it"
)
@click.pass_context
@coro
async def release_rm(ctx: Context, semver: str, force: bool, yes: bool, dry_run: bool) -> None:
    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]
    config = obj["config"]

    if "id" not in config:
        config = await _get_config(config["host"], config["token"], load_tb_file=False)

    current_main_workspace = await get_current_main_workspace(client, config)

    if current_main_workspace["id"] == config["id"] and not force:
        raise CLIReleaseException(
            FeedbackManager.error_exception(error="Use --force to delete a Release in the Main Workspace")
        )

    if yes or click.confirm(FeedbackManager.warning_confirm_delete_release(semver=semver)):
        try:
            response = await client.release_rm(config["id"], semver, confirmation=config["name"], dry_run=dry_run)
            if not dry_run:
                click.echo(FeedbackManager.success_release_delete(semver=semver))
            else:
                click.echo(FeedbackManager.success_release_delete_dry_run(semver=semver))
                if len(response["datasources"]):
                    click.echo("Datasources: " + ", ".join(response["datasources"]))
                if len(response["pipes"]):
                    click.echo("Pipes: " + ", ".join(response["pipes"]))
        except Exception as e:
            raise CLIReleaseException(FeedbackManager.error_exception(error=str(e)))


@cli.group()
@click.pass_context
def env(ctx: Context) -> None:
    """Environment commands. Environments is an experimental feature only available in beta. Running env commands without activation will return an error"""


@env.command(name="ls")
@click.pass_context
@coro
async def branch_ls(ctx: Context) -> None:
    """List all the environments available using the workspace token"""

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client = obj["client"]
    config = obj["config"]

    if "id" not in config:
        config = await _get_config(config["host"], config["token"], load_tb_file=False)

    current_main_workspace = await get_current_main_workspace(client, config)

    if current_main_workspace["id"] != config["id"]:
        client = TinyB(current_main_workspace["token"], config["host"], version=VERSION, send_telemetry=True)

    response = await client.branches()

    columns = ["name", "id", "current"]
    table: List[Tuple[str, str, bool]] = [
        (MAIN_BRANCH, current_main_workspace["id"], config["id"] == current_main_workspace["id"])
    ]

    for branch in response["environments"]:
        table.append((branch["name"], branch["id"], config["id"] == branch["id"]))

    await print_current_workspace(ctx)

    click.echo(FeedbackManager.info_branches())
    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)


@env.command(name="use")
@click.argument("env_name_or_id")
@click.pass_context
@coro
async def branch_use(ctx: Context, env_name_or_id: str) -> None:
    """Switch to another Environment (requires an admin token associated with a user). Use 'tb env ls' to list the Environments you can access"""

    client: TinyB = ctx.ensure_object(dict)["client"]
    config, host, ui_host = await get_config_and_hosts(ctx)

    current_main_workspace = await get_current_main_workspace(client, config)
    if env_name_or_id == MAIN_BRANCH:
        await switch_to_workspace_by_user_workspace_data(ctx, current_main_workspace)
    else:
        await switch_workspace(ctx, env_name_or_id, only_environments=True)


@env.command(name="current")
@click.pass_context
@coro
async def branch_current(ctx: Context) -> None:
    """Show the Environment you're currently authenticated to"""

    await print_current_branch(ctx)


@env.command(name="create", short_help="Create a new Environment in the current 'main' Workspace")
@click.argument("env_name", required=False)
@click.option(
    "--last-partition",
    is_flag=True,
    default=False,
    help="Attach the last modified partition from 'main' to the new Environment",
)
@click.option(
    "--all",
    is_flag=True,
    default=False,
    help="Attach all data from 'main' to the new Environment. Use only if you actually need all the data in the Branch",
)
@click.option(
    "-i",
    "--ignore-datasource",
    "ignore_datasources",
    type=str,
    multiple=True,
    help="Ignore specified data source partitions",
)
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="Wait for data branch jobs to finish, showing a progress bar. Disabled by default.",
)
@click.pass_context
@coro
async def create_branch(
    ctx: Context, env_name: str, last_partition: bool, all: bool, ignore_datasources: List[str], wait: bool
) -> None:
    if last_partition and all:
        click.echo(FeedbackManager.error_exception(error="Use --last-partition or --all but not both"))
        return
    await create_workspace_branch(ctx, env_name, last_partition, all, list(ignore_datasources), wait)


@env.command(name="rm", short_help="Removes an Environment from the Workspace. It can't be recovered.")
@click.argument("env_name_or_id")
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
@click.pass_context
@coro
async def delete_branch(ctx: Context, env_name_or_id: str, yes: bool) -> None:
    """Remove an Environment (not Main)"""

    client: TinyB = ctx.ensure_object(dict)["client"]
    config, _, _ = await get_config_and_hosts(ctx)

    if env_name_or_id == MAIN_BRANCH:
        click.echo(FeedbackManager.error_not_allowed_in_main_branch())
        return

    try:
        workspace_branches = await get_current_workspace_branches(client, config)
        workspace_to_delete = next(
            (
                workspace
                for workspace in workspace_branches
                if workspace["name"] == env_name_or_id or workspace["id"] == env_name_or_id
            ),
            None,
        )
    except Exception as e:
        raise CLIBranchException(FeedbackManager.error_exception(error=str(e)))

    if not workspace_to_delete:
        raise CLIBranchException(FeedbackManager.error_branch(branch=env_name_or_id))

    if yes or click.confirm(FeedbackManager.warning_confirm_delete_branch(branch=workspace_to_delete["name"])):
        need_to_switch_to_main = workspace_to_delete.get("main") and config["id"] == workspace_to_delete["id"]
        # get origin workspace if deleting current branch
        if need_to_switch_to_main:
            try:
                workspaces = (await client.user_workspaces()).get("workspaces", [])
                workspace_main = next(
                    (workspace for workspace in workspaces if workspace["id"] == workspace_to_delete["main"]), None
                )
            except Exception:
                workspace_main = None
        try:
            await client.delete_branch(workspace_to_delete["id"])
            click.echo(FeedbackManager.success_branch_deleted(branch_name=workspace_to_delete["name"]))
        except Exception as e:
            raise CLIBranchException(FeedbackManager.error_exception(error=str(e)))
        else:
            if need_to_switch_to_main:
                if workspace_main:
                    await switch_to_workspace_by_user_workspace_data(ctx, workspace_main)
                else:
                    click.echo(FeedbackManager.error_switching_to_main())


@env.command(
    name="data",
    short_help="Perform a data branch operation to bring data into the current Environment. Check flags for details",
)
@click.option(
    "--last-partition",
    is_flag=True,
    default=False,
    help="Attach the last modified partition from 'main' to the new Environment",
)
@click.option(
    "--all",
    is_flag=True,
    default=False,
    help="Attach all data from 'main' to the new Environment. Use only if you actually need all the data in the Environment",
)
@click.option(
    "-i",
    "--ignore-datasource",
    "ignore_datasources",
    type=str,
    multiple=True,
    help="Ignore specified data source partitions",
)
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="Wait for data branch jobs to finish, showing a progress bar. Disabled by default.",
)
@click.pass_context
@coro
async def data_branch(ctx: Context, last_partition: bool, all: bool, ignore_datasources: List[str], wait: bool) -> None:
    if last_partition and all:
        click.echo(FeedbackManager.error_exception(error="Use --last-partition or --all but not both"))
        return

    if not last_partition and not all:
        click.echo(FeedbackManager.error_exception(error="Use --last-partition or --all"))
        return

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client = obj["client"]
    config = obj["config"]

    current_main_workspace = await get_current_main_workspace(client, config)
    if current_main_workspace["id"] == config["id"]:
        click.echo(FeedbackManager.error_not_allowed_in_main_branch())
        return

    try:
        response = await client.branch_workspace_data(config["id"], last_partition, all, ignore_datasources)

        is_job: bool = "job" in response
        is_summary: bool = "partitions" in response

        if not is_job and not is_summary:
            raise CLIBranchException(response)

        if all and not is_job:
            raise CLIBranchException(response)

        if wait and is_job:
            job_id = response["job"]["job_id"]
            job_url = response["job"]["job_url"]
            click.echo(FeedbackManager.info_data_branch_job_url(url=job_url))
            job_response = await wait_job(client, job_id, job_url, "Data Branching")
            response = job_response["result"]
            is_job = False
            is_summary = "partitions" in response

        if is_job:
            click.echo(FeedbackManager.success_workspace_data_branch_in_progress(job_url=response["job"]["job_url"]))
        else:
            if not is_job and not is_summary:
                FeedbackManager.warning_unknown_response(response=response)
            elif is_summary:
                await print_data_branch_summary(client, None, response)
            click.echo(FeedbackManager.success_workspace_data_branch())

    except Exception as e:
        raise CLIBranchException(FeedbackManager.error_exception(error=str(e)))


@env.group("regression-tests", invoke_without_command=True)
@click.option(
    "-f",
    "--filename",
    type=click.Path(exists=True),
    required=False,
    help="The yaml file with the regression-tests definition",
)
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="Wait for regression job to finish, showing a progress bar. Disabled by default.",
)
@click.pass_context
@coro
async def regression_tests(ctx, filename: str, wait: bool):
    """Regression test commands for Environments"""
    if filename:
        try:
            with open(filename, "r") as file:
                regression_tests_commands = yaml.safe_load(file)
        except Exception as exc:
            raise CLIBranchException(FeedbackManager.error_regression_yaml_not_valid(filename=filename, error=exc))
        if not isinstance(regression_tests_commands, List):
            raise CLIBranchException(
                FeedbackManager.error_regression_yaml_not_valid(filename=filename, error="not a list of pipes")
            )
        client: TinyB = ctx.ensure_object(dict)["client"]
        config = ctx.ensure_object(dict)["config"]

        current_main_workspace = await get_current_main_workspace(client, config)
        if current_main_workspace["id"] == config["id"]:
            click.echo(FeedbackManager.error_not_allowed_in_main_branch())
            return
        try:
            response = await client.branch_regression_tests_file(config["id"], regression_tests_commands)
            if "job" not in response:
                raise CLIBranchException(response)
            job_id = response["job"]["job_id"]
            job_url = response["job"]["job_url"]
            click.echo(FeedbackManager.info_regression_tests_branch_job_url(url=job_url))
            if wait:
                await wait_job(client, job_id, job_url, "Regression tests")
                await print_branch_regression_tests_summary(client, job_id, config["host"])
        except Exception as e:
            raise CLIBranchException(FeedbackManager.error_exception(error=str(e)))
    else:
        if not ctx.invoked_subcommand:
            await _run_regression(ctx, type="coverage", wait=wait)


async def _run_regression(
    ctx: Context,
    type: str,
    pipe_name: Optional[str] = None,
    assert_result: Optional[bool] = True,
    assert_result_no_error: Optional[bool] = True,
    assert_result_rows_count: Optional[bool] = True,
    assert_result_ignore_order: Optional[bool] = False,
    assert_time_increase_percentage: Optional[int] = 25,
    assert_bytes_read_increase_percentage: Optional[int] = 25,
    failfast: Optional[bool] = False,
    wait: Optional[bool] = False,
    **kwargs,
):
    client: TinyB = ctx.ensure_object(dict)["client"]
    config = ctx.ensure_object(dict)["config"]

    current_main_workspace = await get_current_main_workspace(client, config)
    if current_main_workspace["id"] == config["id"]:
        click.echo(FeedbackManager.error_not_allowed_in_main_branch())
        return
    try:
        response = await client.branch_regression_tests(
            config["id"],
            pipe_name,
            type,
            failfast=failfast,
            assert_result=assert_result,
            assert_result_no_error=assert_result_no_error,
            assert_result_rows_count=assert_result_rows_count,
            assert_result_ignore_order=assert_result_ignore_order,
            assert_time_increase_percentage=assert_time_increase_percentage,
            assert_bytes_read_increase_percentage=assert_bytes_read_increase_percentage,
            **kwargs,
        )
        if "job" not in response:
            raise CLIBranchException(response)
        job_id = response["job"]["job_id"]
        job_url = response["job"]["job_url"]
        click.echo(FeedbackManager.info_regression_tests_branch_job_url(url=job_url))
        if wait:
            await wait_job(client, job_id, job_url, "Regression tests")
            await print_branch_regression_tests_summary(client, job_id, config["host"])
    except Exception as e:
        raise CLIBranchException(FeedbackManager.error_exception(error=str(e)))


@regression_tests.command(
    name="coverage",
    short_help="Run regression tests using coverage requests for Environment vs Main Workspace. It creates a regression-tests job. The argument pipe_name supports regular expressions. Using '.*' if no pipe_name is provided",
)
@click.argument("pipe_name", required=False)
@click.option(
    "--assert-result/--no-assert-result",
    is_flag=True,
    default=True,
    help="Whether to perform an assertion on the results returned by the endpoint. Enabled by default. Use --no-assert-result if you expect the endpoint output is different from current version",
)
@click.option(
    "--assert-result-no-error/--no-assert-result-no-error",
    is_flag=True,
    default=True,
    help="Whether to verify that the endpoint does not return errors. Enabled by default. Use --no-assert-result-no-error if you expect errors from the endpoint",
)
@click.option(
    "--assert-result-rows-count/--no-assert-result-rows-count",
    is_flag=True,
    default=True,
    help="Whether to verify that the correct number of elements are returned in the results. Enabled by default. Use --no-assert-result-rows-count if you expect the numbers of elements in the endpoint output is different from current version",
)
@click.option(
    "--assert-result-ignore-order/--no-assert-result-ignore-order",
    is_flag=True,
    default=False,
    help="Whether to ignore the order of the elements in the results. Disabled by default. Use --assert-result-ignore-order if you expect the endpoint output is returning same elements but in different order",
)
@click.option(
    "--assert-time-increase-percentage",
    type=int,
    required=False,
    default=25,
    help="Allowed percentage increase in endpoint response time. Default value is 25%. Use -1 to disable assert.",
)
@click.option(
    "--assert-bytes-read-increase-percentage",
    type=int,
    required=False,
    default=25,
    help="Allowed percentage increase in the amount of bytes read by the endpoint. Default value is 25%. Use -1 to disable assert",
)
@click.option(
    "-ff", "--failfast", is_flag=True, default=False, help="When set, the checker will exit as soon one test fails"
)
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="Waits for regression job to finish, showing a progress bar. Disabled by default.",
)
@click.pass_context
@coro
async def coverage(
    ctx: Context,
    pipe_name: str,
    assert_result: bool,
    assert_result_no_error: bool,
    assert_result_rows_count: bool,
    assert_result_ignore_order: bool,
    assert_time_increase_percentage: int,
    assert_bytes_read_increase_percentage: int,
    failfast: bool,
    wait: bool,
):
    await _run_regression(
        ctx,
        "coverage",
        pipe_name,
        assert_result,
        assert_result_no_error,
        assert_result_rows_count,
        assert_result_ignore_order,
        assert_time_increase_percentage,
        assert_bytes_read_increase_percentage,
        failfast,
        wait,
    )


@regression_tests.command(
    name="last",
    short_help="Run regression tests using last requests for Environment vs Main Workspace. It creates a regression-tests job. The argument pipe_name supports regular expressions. Using '.*' if no pipe_name is provided",
)
@click.argument("pipe_name", required=False)
@click.option(
    "-l",
    "--limit",
    type=click.IntRange(1, 100),
    default=10,
    required=False,
    help="Number of requests to validate. Default is 10",
)
@click.option(
    "--assert-result/--no-assert-result",
    is_flag=True,
    default=True,
    help="Whether to perform an assertion on the results returned by the endpoint. Enabled by default. Use --no-assert-result if you expect the endpoint output is different from current version",
)
@click.option(
    "--assert-result-no-error/--no-assert-result-no-error",
    is_flag=True,
    default=True,
    help="Whether to verify that the endpoint does not return errors. Enabled by default. Use --no-assert-result-no-error if you expect errors from the endpoint",
)
@click.option(
    "--assert-result-rows-count/--no-assert-result-rows-count",
    is_flag=True,
    default=True,
    help="Whether to verify that the correct number of elements are returned in the results. Enabled by default. Use --no-assert-result-rows-count if you expect the numbers of elements in the endpoint output is different from current version",
)
@click.option(
    "--assert-result-ignore-order/--no-assert-result-ignore-order",
    is_flag=True,
    default=False,
    help="Whether to ignore the order of the elements in the results. Disabled by default. Use --assert-result-ignore-order if you expect the endpoint output is returning same elements but in different order",
)
@click.option(
    "--assert-time-increase-percentage",
    type=int,
    required=False,
    default=25,
    help="Allowed percentage increase in endpoint response time. Default value is 25%. Use -1 to disable assert.",
)
@click.option(
    "--assert-bytes-read-increase-percentage",
    type=int,
    required=False,
    default=25,
    help="Allowed percentage increase in the amount of bytes read by the endpoint. Default value is 25%. Use -1 to disable assert",
)
@click.option(
    "-ff", "--failfast", is_flag=True, default=False, help="When set, the checker will exit as soon one test fails"
)
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="Waits for regression job to finish, showing a progress bar. Disabled by default.",
)
@click.pass_context
@coro
async def last(
    ctx: Context,
    pipe_name: str,
    limit: int,
    assert_result: bool,
    assert_result_no_error: bool,
    assert_result_rows_count: bool,
    assert_result_ignore_order: bool,
    assert_time_increase_percentage: int,
    assert_bytes_read_increase_percentage: int,
    failfast: bool,
    wait: bool,
):
    await _run_regression(
        ctx,
        "last",
        pipe_name,
        assert_result,
        assert_result_no_error,
        assert_result_rows_count,
        assert_result_ignore_order,
        assert_time_increase_percentage,
        assert_bytes_read_increase_percentage,
        failfast,
        wait,
        limit=limit,
    )


@regression_tests.command(
    name="manual",
    short_help="Run regression tests using manual requests for Environment vs Main Workspace. It creates a regression-tests job. The argument pipe_name supports regular expressions. Using '.*' if no pipe_name is provided",
    context_settings=dict(allow_extra_args=True, ignore_unknown_options=True),
)
@click.argument("pipe_name", required=False)
@click.option(
    "--assert-result/--no-assert-result",
    is_flag=True,
    default=True,
    help="Whether to perform an assertion on the results returned by the endpoint. Enabled by default. Use --no-assert-result if you expect the endpoint output is different from current version",
)
@click.option(
    "--assert-result-no-error/--no-assert-result-no-error",
    is_flag=True,
    default=True,
    help="Whether to verify that the endpoint does not return errors. Enabled by default. Use --no-assert-result-no-error if you expect errors from the endpoint",
)
@click.option(
    "--assert-result-rows-count/--no-assert-result-rows-count",
    is_flag=True,
    default=True,
    help="Whether to verify that the correct number of elements are returned in the results. Enabled by default. Use --no-assert-result-rows-count if you expect the numbers of elements in the endpoint output is different from current version",
)
@click.option(
    "--assert-result-ignore-order/--no-assert-result-ignore-order",
    is_flag=True,
    default=False,
    help="Whether to ignore the order of the elements in the results. Disabled by default. Use --assert-result-ignore-order if you expect the endpoint output is returning same elements but in different order",
)
@click.option(
    "--assert-time-increase-percentage",
    type=int,
    required=False,
    default=25,
    help="Allowed percentage increase in endpoint response time. Default value is 25%. Use -1 to disable assert.",
)
@click.option(
    "--assert-bytes-read-increase-percentage",
    type=int,
    required=False,
    default=25,
    help="Allowed percentage increase in the amount of bytes read by the endpoint. Default value is 25%. Use -1 to disable assert",
)
@click.option(
    "-ff", "--failfast", is_flag=True, default=False, help="When set, the checker will exit as soon one test fails"
)
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="Waits for regression job to finish, showing a progress bar. Disabled by default.",
)
@click.pass_context
@coro
async def manual(
    ctx: Context,
    pipe_name: str,
    assert_result: bool,
    assert_result_no_error: bool,
    assert_result_rows_count: bool,
    assert_result_ignore_order: bool,
    assert_time_increase_percentage: int,
    assert_bytes_read_increase_percentage: int,
    failfast: bool,
    wait: bool,
):
    params = [{ctx.args[i][2:]: ctx.args[i + 1] for i in range(0, len(ctx.args), 2)}]
    await _run_regression(
        ctx,
        "manual",
        pipe_name,
        assert_result,
        assert_result_no_error,
        assert_result_rows_count,
        assert_result_ignore_order,
        assert_time_increase_percentage,
        assert_bytes_read_increase_percentage,
        failfast,
        wait,
        params=params,
    )


@env.group()
@click.pass_context
def datasource(ctx: Context) -> None:
    """Environment data source commands."""


@datasource.command(name="copy")
@click.argument("datasource_name")
@click.option(
    "--sql",
    default=None,
    help="Freeform SQL query to select what is copied from Main into the Environment Data Source",
    required=False,
)
@click.option(
    "--sql-from-main",
    is_flag=True,
    default=False,
    help="SQL query selecting * from the same Data Source in Main",
    required=False,
)
@click.option("--wait", is_flag=True, default=False, help="Wait for copy job to finish, disabled by default")
@click.option(
    "--semver",
    is_flag=False,
    required=False,
    type=str,
    help="Release semver where to run the copy operation. Example: 1.0.0",
)
@click.pass_context
@coro
async def datasource_copy_from_main(
    ctx: Context, datasource_name: str, sql: str, sql_from_main: bool, wait: bool, semver: str
) -> None:
    """Copy data source from Main."""

    client: TinyB = ctx.ensure_object(dict)["client"]
    config = ctx.ensure_object(dict)["config"]

    if sql and sql_from_main:
        click.echo(FeedbackManager.error_exception(error="Use --sql or --sql-from-main but not both"))
        return

    if not sql and not sql_from_main:
        click.echo(FeedbackManager.error_exception(error="Use --sql or --sql-from-main"))
        return

    current_main_workspace = await get_current_main_workspace(client, config)
    if current_main_workspace["id"] == config["id"] and sql_from_main:
        click.echo(FeedbackManager.error_not_allowed_in_main_branch())
        return

    response = await client.datasource_query_copy(
        datasource_name, sql if sql else f"SELECT * FROM main.{datasource_name}", semver
    )
    if "job" not in response:
        raise CLIBranchException(response)
    job_id = response["job"]["job_id"]
    job_url = response["job"]["job_url"]
    if sql:
        click.echo(FeedbackManager.info_copy_with_sql_job_url(sql=sql, datasource_name=datasource_name, url=job_url))
    else:
        click.echo(FeedbackManager.info_copy_from_main_job_url(datasource_name=datasource_name, url=job_url))
    if wait:
        base_msg = "Copy from Main Workspace" if sql_from_main else f"Copy from {sql}"
        await wait_job(client, job_id, job_url, f"{base_msg} to {datasource_name}")


@env.command(name="deploy", short_help="Deploys a new Release. It creates a deployment job", hidden=True)
@click.option("--semver", is_flag=False, required=True, type=str, help="Semver for this version. Example: 1.0.0")
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="Waits for deployment job to finish, showing a progress bar. Disabled by default.",
)
@click.option("--verbose", is_flag=True, default=False, help="Print DEBUG logs.")
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="dry_run mode. It does not run the deployment job, but it prints the steps to deploy and the data migrations to run. Default value is False.",
)
@click.option(
    "--migrations",
    type=click.Path(exists=True),
    required=False,
    help="The yaml file with the data migrations definition",
)
@click.pass_context
@coro
async def deploy_env(ctx: Context, semver: str, wait: bool, verbose: bool, dry_run: bool, migrations: str) -> None:
    client: TinyB = ctx.ensure_object(dict)["client"]
    config = ctx.ensure_object(dict)["config"]

    current_main_workspace = await get_current_main_workspace(client, config)
    if current_main_workspace["id"] == config["id"]:
        click.echo(FeedbackManager.error_not_allowed_in_main_branch())
        return

    workspaces: List[Dict[str, Any]] = (await client.user_workspaces_and_branches()).get("workspaces", [])
    current_ws: Dict[str, Any] = next(
        (workspace for workspace in workspaces if config and workspace.get("id", ".") == config.get("id", "..")), {}
    )

    current_release = current_ws.get("release")
    if not current_release:
        raise CLIGitReleaseException(FeedbackManager.error_init_release(workspace=current_ws["name"]))
    cli_git_release = CLIGitRelease()
    cli_git_release.validate_local_for_release(current_release, check_new=False)
    commit = cli_git_release.head().commit.hexsha

    data_migrations = None
    if migrations:
        with open(migrations, "r") as file:
            data_migrations = json.loads(file.read())

    await deploy_environment(
        ctx, config["id"], current_main_workspace, wait, verbose, commit, semver, data_migrations, dry_run
    )
