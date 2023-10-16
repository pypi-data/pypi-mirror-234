# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import json
import os
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple
import click
from click import Context
import tinybird.context as context

import humanfriendly
from tinybird.client import DoesNotExistException, TinyB
from tinybird.config import DEFAULT_API_HOST, FeatureFlags
from tinybird.datafile import folder_push, wait_job, get_name_tag_version, process_file
from tinybird.tb_cli_modules.cli import cli
from tinybird.tb_cli_modules.common import coro, create_tb_client, echo_safe_humanfriendly_tables_format_smart_table
from tinybird.feedback_manager import FeedbackManager
from tinybird.tb_cli_modules.exceptions import CLIPipeException


@cli.group()
@click.pass_context
def pipe(ctx):
    """Pipes commands"""


@pipe.group(name="copy")
@click.pass_context
def pipe_copy(ctx: Context) -> None:
    """Copy Pipe commands"""


@pipe.group(name="sink", hidden=True)
@click.pass_context
def pipe_sink(ctx: Context) -> None:
    """Sink Pipe commands"""


@pipe.command(
    name="generate",
    short_help="Generates a pipe file based on a sql query. Example: tb pipe generate my_pipe 'select * from existing_datasource'",
)
@click.argument("name")
@click.argument("query")
@click.option("--force", is_flag=True, default=False, help="Override existing files")
@click.pass_context
def generate_pipe(ctx: click.Context, name: str, query: str, force: bool):
    pipefile = f"""
NODE endpoint
DESCRIPTION >
    Generated from the command line
SQL >
    {query}

    """
    base = Path("endpoints")
    if not base.exists():
        base = Path()
    f = base / (f"{name}.pipe")
    if not f.exists() or force:
        with open(f"{f}", "w") as file:
            file.write(pipefile)
        click.echo(FeedbackManager.success_generated_pipe(file=f))
    else:
        click.echo(FeedbackManager.error_exception(error=f"File {f} already exists, use --force to override"))


@pipe.command(name="stats")
@click.argument("pipes", nargs=-1)
@click.option(
    "--format",
    "format_",
    type=click.Choice(["json"], case_sensitive=False),
    default=None,
    help="Force a type of the output. To parse the output, keep in mind to use `tb --no-version-warning pipe stats`  option.",
)
@click.pass_context
@coro
async def pipe_stats(ctx: click.Context, pipes: Tuple[str, ...], format_: str):
    """
    Print pipe stats for the last 7 days
    """
    client: TinyB = ctx.ensure_object(dict)["client"]
    all_pipes = await client.pipes()
    pipes_to_get_stats = []
    pipes_ids: Dict = {}

    if pipes:
        # We filter by the pipes we want to look for
        all_pipes = [pipe for pipe in all_pipes if pipe["name"] in pipes]

    for pipe in all_pipes:
        name_tag = get_name_tag_version(pipe["name"], ignore_prefix=True)
        if name_tag["name"] in pipe["name"]:
            pipes_to_get_stats.append(f"'{pipe['id']}'")
            pipes_ids[pipe["id"]] = name_tag

    if not pipes_to_get_stats:
        if format_ == "json":
            click.echo(json.dumps({"pipes": []}, indent=2))
        else:
            click.echo(FeedbackManager.info_no_pipes_stats())
        return

    sql = f"""
        SELECT
            pipe_id id,
            sumIf(view_count, date > now() - interval 7 day) requests,
            sumIf(error_count, date > now() - interval 7 day) errors,
            avgMergeIf(avg_duration_state, date > now() - interval 7 day) latency
        FROM tinybird.pipe_stats
        WHERE pipe_id in ({','.join(pipes_to_get_stats)})
        GROUP BY pipe_id
        ORDER BY requests DESC
        FORMAT JSON
    """

    res = await client.query(sql)

    if res and "error" in res:
        click.echo(FeedbackManager.error_exception(error=str(res["error"])))
        return

    columns = ["prefix", "version", "name", "request count", "error count", "avg latency"]
    table_human_readable: List[Tuple] = []
    table_machine_readable: List[Dict] = []
    if res and "data" in res:
        for x in res["data"]:
            tk = pipes_ids[x["id"]]
            table_human_readable.append(
                (
                    tk["tag"] or "",
                    tk["version"] if tk["version"] is not None else "",
                    tk["name"],
                    x["requests"],
                    x["errors"],
                    x["latency"],
                )
            )
            table_machine_readable.append(
                {
                    "prefix": tk["tag"] or "",
                    "version": tk["version"] if tk["version"] is not None else "",
                    "name": tk["name"],
                    "requests": x["requests"],
                    "errors": x["errors"],
                    "latency": x["latency"],
                }
            )

        table_human_readable.sort(key=lambda x: (x[2], x[1]))
        table_machine_readable.sort(key=lambda x: x["name"])

        if format_ == "json":
            click.echo(json.dumps({"pipes": table_machine_readable}, indent=2))
        else:
            echo_safe_humanfriendly_tables_format_smart_table(table_human_readable, column_names=columns)


@pipe.command(name="ls")
@click.option("--prefix", default=None, help="Show only resources with this prefix", hidden=True)
@click.option("--match", default=None, help="Retrieve any resourcing matching the pattern. eg --match _test")
@click.option(
    "--format",
    "format_",
    type=click.Choice(["json"], case_sensitive=False),
    default=None,
    help="Force a type of the output",
)
@click.pass_context
@coro
async def pipe_ls(ctx: Context, prefix: str, match: str, format_: str):
    """List pipes"""
    if prefix:
        click.echo(
            FeedbackManager.warning_deprecated(
                warning="The `--prefix` flag is deprecated and EOL is planned for 20th of Dec. You should use different workspaces instead, see this migration guide for more info => https://www.tinybird.co/docs/guides/staging-and-production-workspaces.html#migrating-from-prefixes"
            )
        )

    client: TinyB = ctx.ensure_object(dict)["client"]
    pipes = await client.pipes(dependencies=False, node_attrs="name", attrs="name,updated_at")
    pipes = sorted(pipes, key=lambda p: p["updated_at"])

    columns = ["version", "name", "published date", "nodes"]
    table_human_readable = []
    table_machine_readable = []
    pattern = re.compile(match) if match else None
    for t in pipes:
        tk = get_name_tag_version(t["name"], ignore_prefix=prefix is None)
        if (prefix and tk["tag"] != prefix) or (pattern and not pattern.search(tk["name"])):
            continue
        table_human_readable.append(
            (tk["version"] if tk["version"] is not None else "", tk["name"], t["updated_at"][:-7], len(t["nodes"]))
        )
        table_machine_readable.append(
            {
                "version": tk["version"] if tk["version"] is not None else "",
                "name": tk["name"],
                "published date": t["updated_at"][:-7],
                "nodes": len(t["nodes"]),
            }
        )

    if not format_:
        click.echo(FeedbackManager.info_pipes())
        echo_safe_humanfriendly_tables_format_smart_table(table_human_readable, column_names=columns)
        click.echo("\n")
    elif format_ == "json":
        click.echo(json.dumps({"pipes": table_machine_readable}, indent=2))
    else:
        click.echo(FeedbackManager.error_pipe_ls_type)


@pipe.command(name="populate")
@click.argument("pipe_name")
@click.option("--node", type=str, help="Name of the materialized node.")
@click.option(
    "--sql-condition",
    type=str,
    default=None,
    help="Populate with a SQL condition to be applied to the trigger Data Source of the Materialized View. For instance, `--sql-condition='date == toYYYYMM(now())'` it'll populate taking all the rows from the trigger Data Source which `date` is the current month. Use it together with --populate. --sql-condition is not taken into account if the --subset param is present. Including in the ``sql_condition`` any column present in the Data Source ``engine_sorting_key`` will make the populate job process less data.",
)
@click.option(
    "--truncate", is_flag=True, default=False, help="Truncates the materialized Data Source before populating it."
)
@click.option(
    "--unlink-on-populate-error",
    is_flag=True,
    default=False,
    help="If the populate job fails the Materialized View is unlinked and new data won't be ingested in the Materialized View. First time a populate job fails, the Materialized View is always unlinked.",
)
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="Waits for populate jobs to finish, showing a progress bar. Disabled by default.",
)
@click.option(
    "--semver",
    is_flag=False,
    required=False,
    type=str,
    help="Semver of a preview Release to run the population. Example: 1.0.0",
    hidden=True,
)
@click.pass_context
@coro
async def pipe_populate(
    ctx: click.Context,
    pipe_name: str,
    node: str,
    sql_condition: str,
    truncate: bool,
    unlink_on_populate_error: bool,
    wait: bool,
    semver: str,
):
    """Populate the result of a Materialized Node into the target Materialized View"""
    cl = create_tb_client(ctx)
    response = await cl.populate_node(
        pipe_name,
        node,
        populate_condition=sql_condition,
        truncate=truncate,
        unlink_on_populate_error=unlink_on_populate_error,
        semver=semver,
    )
    if "job" not in response:
        raise CLIPipeException(response)

    job_id = response["job"]["id"]
    job_url = response["job"]["job_url"]
    if sql_condition:
        click.echo(FeedbackManager.info_populate_condition_job_url(url=job_url, populate_condition=sql_condition))
    else:
        click.echo(FeedbackManager.info_populate_job_url(url=job_url))
    if wait:
        await wait_job(cl, job_id, job_url, "Populating", semver=semver)


@pipe.command(name="new", hidden=True)
@click.argument("pipe_name")
@click.argument("sql")
@click.pass_context
@coro
async def pipe_create(ctx: click.Context, pipe_name: str, sql: str):
    """Create a new pipe"""
    click.echo(FeedbackManager.warning_deprecated(warning="This command is deprecated."))
    client: TinyB = ctx.ensure_object(dict)["client"]
    host = ctx.ensure_object(dict)["config"].get("host", DEFAULT_API_HOST)
    res = await client.pipe_create(pipe_name, sql)
    click.echo(FeedbackManager.success_created_pipe(pipe=pipe_name, node_id=res["nodes"][0]["id"], host=host))


@pipe.command(name="append")
@click.argument("pipe_name_or_uid")
@click.argument("sql")
@click.pass_context
@coro
async def pipe_append_node(ctx: click.Context, pipe_name_or_uid: str, sql: str):
    """Append a node to a pipe"""
    client = ctx.ensure_object(dict)["client"]
    try:
        res = await client.pipe_append_node(pipe_name_or_uid, sql)
        click.echo(
            FeedbackManager.success_node_changed(
                pipe_name_or_uid=pipe_name_or_uid, node_name=res["name"], node_id=res["id"]
            )
        )
    except DoesNotExistException:
        raise CLIPipeException(FeedbackManager.error_pipe_does_not_exist(pipe=pipe_name_or_uid))


async def common_pipe_publish_node(ctx: click.Context, pipe_name_or_id: str, node_uid: Optional[str] = None):
    """Change the published node of a pipe"""
    client: TinyB = ctx.ensure_object(dict)["client"]
    host = ctx.ensure_object(dict)["config"].get("host", DEFAULT_API_HOST)

    try:
        pipe = await client.pipe(pipe_name_or_id)
        if not node_uid:
            node = pipe["nodes"][-1]["name"]
            click.echo(FeedbackManager.info_using_node(node=node))
        else:
            node = node_uid

        await client.pipe_set_endpoint(pipe_name_or_id, node)
        click.echo(FeedbackManager.success_node_published(pipe=pipe_name_or_id, host=host))
    except DoesNotExistException:
        raise CLIPipeException(FeedbackManager.error_pipe_does_not_exist(pipe=pipe_name_or_id))
    except Exception as e:
        raise CLIPipeException(FeedbackManager.error_exception(error=e))


@pipe.command(name="publish")
@click.argument("pipe_name_or_id")
@click.argument("node_uid", default=None, required=False)
@click.pass_context
@coro
async def pipe_publish_node(ctx: click.Context, pipe_name_or_id: str, node_uid: Optional[str] = None):
    """Change the published node of a pipe"""
    await common_pipe_publish_node(ctx, pipe_name_or_id, node_uid)


@pipe.command(name="unpublish")
@click.argument("pipe_name_or_id")
@click.argument("node_uid", default=None, required=False)
@click.pass_context
@coro
async def pipe_unpublish_node(ctx: click.Context, pipe_name_or_id: str, node_uid: Optional[str] = None):
    """Unpublish the endpoint of a pipe"""
    client: TinyB = ctx.ensure_object(dict)["client"]
    host = ctx.ensure_object(dict)["config"].get("host", DEFAULT_API_HOST)

    try:
        pipe = await client.pipe(pipe_name_or_id)

        if not pipe["endpoint"]:
            raise CLIPipeException(FeedbackManager.error_remove_no_endpoint())

        if not node_uid:
            node = pipe["endpoint"]
            click.echo(FeedbackManager.info_using_node(node=node))
        else:
            node = node_uid

        await client.pipe_remove_endpoint(pipe_name_or_id, node)
        click.echo(FeedbackManager.success_node_unpublished(pipe=pipe_name_or_id, host=host))
    except DoesNotExistException:
        raise CLIPipeException(FeedbackManager.error_pipe_does_not_exist(pipe=pipe_name_or_id))
    except Exception as e:
        raise CLIPipeException(FeedbackManager.error_exception(error=e))


@pipe.command(name="set_endpoint")
@click.argument("pipe_name_or_id")
@click.argument("node_uid", default=None, required=False)
@click.pass_context
@coro
async def pipe_published_node(ctx: click.Context, pipe_name_or_id: str, node_uid: Optional[str] = None):
    """Same as 'publish', change the published node of a pipe"""
    await common_pipe_publish_node(ctx, pipe_name_or_id, node_uid)


@pipe.command(name="rm")
@click.argument("pipe_name_or_id")
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
@click.pass_context
@coro
async def pipe_delete(ctx: click.Context, pipe_name_or_id: str, yes: bool):
    """Delete a pipe. pipe_name_or_id can be either a Pipe name or id in the Workspace or a local path to a .pipe file"""

    client: TinyB = ctx.ensure_object(dict)["client"]

    file_path = pipe_name_or_id
    if os.path.exists(file_path):
        result = await process_file(file_path, client)
        pipe_name_or_id = result[0]["name"]

    if yes or click.confirm(FeedbackManager.warning_confirm_delete_pipe(pipe=pipe_name_or_id)):
        try:
            await client.pipe_delete(pipe_name_or_id)
        except DoesNotExistException:
            raise CLIPipeException(FeedbackManager.error_pipe_does_not_exist(pipe=pipe_name_or_id))

        click.echo(FeedbackManager.success_delete_pipe(pipe=pipe_name_or_id))


@pipe.command(name="token_read")
@click.argument("pipe_name")
@click.pass_context
@coro
async def pipe_token_read(ctx: click.Context, pipe_name: str):
    """Retrieve a token to read a pipe"""
    client: TinyB = ctx.ensure_object(dict)["client"]

    try:
        await client.pipe_file(pipe_name)
    except DoesNotExistException:
        raise CLIPipeException(FeedbackManager.error_pipe_does_not_exist(pipe=pipe_name))

    tokens = await client.tokens()
    token = None

    for t in tokens:
        for scope in t["scopes"]:
            if scope["type"] == "PIPES:READ" and scope["resource"] == pipe_name:
                token = t["token"]
    if token:
        click.echo(token)
    else:
        click.echo(FeedbackManager.warning_token_pipe(pipe=pipe_name))


@pipe.command(
    name="data",
    context_settings=dict(
        allow_extra_args=True,
        ignore_unknown_options=True,
    ),
)
@click.argument("pipe")
@click.option("--query", default=None, help="Run SQL over pipe results")
@click.option(
    "--format", "format_", type=click.Choice(["json", "csv"], case_sensitive=False), help="Return format (CSV, JSON)"
)
@click.pass_context
@coro
async def print_pipe(ctx: Context, pipe: str, query: str, format_: str):
    """Print data returned by a pipe

    Syntax: tb pipe data <pipe_name> --param_name value --param2_name value2 ...
    """

    client: TinyB = ctx.ensure_object(dict)["client"]
    params = {ctx.args[i][2:]: ctx.args[i + 1] for i in range(0, len(ctx.args), 2)}
    req_format = "json" if not format_ else format_.lower()
    try:
        res = await client.pipe_data(pipe, format=req_format, sql=query, params=params)
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return

    if not format_:
        stats = res["statistics"]
        seconds = stats["elapsed"]
        rows_read = humanfriendly.format_number(stats["rows_read"])
        bytes_read = humanfriendly.format_size(stats["bytes_read"])

        click.echo(FeedbackManager.success_print_pipe(pipe=pipe))
        click.echo(FeedbackManager.info_query_stats(seconds=seconds, rows=rows_read, bytes=bytes_read))

        if not res["data"]:
            click.echo(FeedbackManager.info_no_rows())
        else:
            echo_safe_humanfriendly_tables_format_smart_table(
                data=[d.values() for d in res["data"]], column_names=res["data"][0].keys()
            )
        click.echo("\n")
    elif req_format == "json":
        click.echo(json.dumps(res))
    else:
        click.echo(res)


@pipe.command(name="regression-test", short_help="Run regression tests using last requests")
@click.option("--prefix", default="", help="Use prefix for all the resources", hidden=True)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Prints internal representation, can be combined with any command to get more information.",
)
@click.option("--only-response-times", is_flag=True, default=False, help="Checks only response times")
@click.argument("filenames", type=click.Path(exists=True), nargs=-1, default=None)
@click.option("--workspace_map", nargs=2, type=str, multiple=True)
@click.option(
    "--workspace",
    nargs=2,
    type=str,
    multiple=True,
    help="add a workspace path to the list of external workspaces, usage: --workspace name path/to/folder",
)
@click.option(
    "--no-versions",
    is_flag=True,
    default=False,
    help="when set, resource dependency versions are not used, it pushes the dependencies as-is",
)
@click.option(
    "-l", "--limit", type=click.IntRange(0, 100), default=0, required=False, help="Number of requests to validate"
)
@click.option(
    "--sample-by-params",
    type=click.IntRange(1, 100),
    default=1,
    required=False,
    help="When set, we will aggregate the pipe_stats_rt requests by extractURLParameterNames(assumeNotNull(url)) and for each combination we will take a sample of N requests",
)
@click.option(
    "-m",
    "--match",
    multiple=True,
    required=False,
    help="Filter the checker requests by specific parameter. You can pass multiple parameters -m foo -m bar",
)
@click.option(
    "-ff", "--failfast", is_flag=True, default=False, help="When set, the checker will exit as soon one test fails"
)
@click.option(
    "--ignore-order", is_flag=True, default=False, help="When set, the checker will ignore the order of list properties"
)
@click.option(
    "--validate-processed-bytes",
    is_flag=True,
    default=False,
    help="When set, the checker will validate that the new version doesn't process more than 25% than the current version",
)
@click.option(
    "--check-requests-from-main",
    is_flag=True,
    default=False,
    help="When set, the checker will get Main Workspace requests",
    hidden=True,
)
@click.pass_context
@coro
async def regression_test(
    ctx: click.Context,
    prefix: str,
    filenames: Optional[List[str]],
    debug: bool,
    only_response_times: bool,
    workspace_map,
    workspace: str,
    no_versions: bool,
    limit: int,
    sample_by_params: int,
    match: List[str],
    failfast: bool,
    ignore_order: bool,
    validate_processed_bytes: bool,
    check_requests_from_main: bool,
):
    """
    Run regression tests on Tinybird
    """
    if prefix:
        click.echo(
            FeedbackManager.warning_deprecated(
                warning="The `--prefix` flag is deprecated and EOL is planned for 20th of Dec. You should use different workspaces instead, see this migration guide for more info => https://www.tinybird.co/docs/guides/staging-and-production-workspaces.html#migrating-from-prefixes"
            )
        )

    ignore_sql_errors = FeatureFlags.ignore_sql_errors()

    context.disable_template_security_validation.set(True)
    await folder_push(
        create_tb_client(ctx),
        prefix,
        filenames,
        dry_run=False,
        check=True,
        push_deps=False,
        debug=debug,
        force=False,
        populate=False,
        upload_fixtures=False,
        wait=False,
        ignore_sql_errors=ignore_sql_errors,
        skip_confirmation=False,
        only_response_times=only_response_times,
        workspace_map=dict(workspace_map),
        workspace_lib_paths=workspace,
        no_versions=no_versions,
        timeout=False,
        run_tests=True,
        tests_to_run=limit,
        tests_sample_by_params=sample_by_params,
        tests_filter_by=match,
        tests_failfast=failfast,
        tests_ignore_order=ignore_order,
        tests_validate_processed_bytes=validate_processed_bytes,
        tests_check_requests_from_branch=check_requests_from_main,
    )
    return


@pipe_copy.command(name="run", short_help="Run an on-demand copy job")
@click.argument("pipe_name_or_id")
@click.option("--wait", is_flag=True, default=False, help="Wait for the copy job to finish")
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
@click.option(
    "--param",
    nargs=1,
    type=str,
    multiple=True,
    default=None,
    help="Key and value of the params you want the Copy pipe to be called with. For example: tb pipe copy run <my_copy_pipe> --param foo=bar",
)
@click.pass_context
@coro
async def pipe_copy_run(ctx: click.Context, pipe_name_or_id: str, wait: bool, yes: bool, param: Optional[Tuple[str]]):
    """Run an on-demand copy job"""

    params = dict(key_value.split("=") for key_value in param) if param else {}

    if yes or click.confirm(FeedbackManager.warning_confirm_copy_pipe(pipe=pipe_name_or_id)):
        click.echo(FeedbackManager.info_copy_job_running(pipe=pipe_name_or_id))
        client: TinyB = ctx.ensure_object(dict)["client"]

        try:
            response = await client.pipe_run_copy(pipe_name_or_id, params)

            job_id = response["job"]["job_id"]
            job_url = response["job"]["job_url"]
            target_datasource_id = response["tags"]["copy_target_datasource"]
            target_datasource = await client.get_datasource(target_datasource_id)
            target_datasource_name = target_datasource["name"]
            click.echo(
                FeedbackManager.success_copy_job_created(target_datasource=target_datasource_name, job_id=job_id)
            )

            if wait:
                await wait_job(client, job_id, job_url, "** Copying data")
                click.echo(FeedbackManager.success_data_copied_to_ds(target_datasource=target_datasource_name))

        except Exception as e:
            raise CLIPipeException(FeedbackManager.error_creating_copy_job(error=e))


@pipe_copy.command(name="resume", short_help="Resume a paused copy pipe")
@click.argument("pipe_name_or_id")
@click.pass_context
@coro
async def pipe_copy_resume(ctx: click.Context, pipe_name_or_id: str):
    """Resume a paused copy pipe"""

    click.echo(FeedbackManager.info_copy_pipe_resuming(pipe=pipe_name_or_id))
    client: TinyB = ctx.ensure_object(dict)["client"]

    try:
        await client.pipe_resume_copy(pipe_name_or_id)
        click.echo(FeedbackManager.success_copy_pipe_resumed(pipe=pipe_name_or_id))

    except Exception as e:
        raise CLIPipeException(FeedbackManager.error_resuming_copy_pipe(error=e))


@pipe_copy.command(name="pause", short_help="Pause a running copy pipe")
@click.argument("pipe_name_or_id")
@click.pass_context
@coro
async def pipe_copy_pause(ctx: click.Context, pipe_name_or_id: str):
    """Pause a running copy pipe"""

    click.echo(FeedbackManager.info_copy_pipe_pausing(pipe=pipe_name_or_id))
    client: TinyB = ctx.ensure_object(dict)["client"]

    try:
        await client.pipe_pause_copy(pipe_name_or_id)
        click.echo(FeedbackManager.success_copy_pipe_paused(pipe=pipe_name_or_id))

    except Exception as e:
        raise CLIPipeException(FeedbackManager.error_pausing_copy_pipe(error=e))


@pipe_sink.command(name="run", short_help="Run an on-demand sink job")
@click.argument("pipe_name_or_id")
@click.option("--wait", is_flag=True, default=False, help="Wait for the sink job to finish")
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
@click.option(
    "--param",
    nargs=1,
    type=str,
    multiple=True,
    default=None,
    help="Key and value of the params you want the Sink pipe to be called with. For example: tb pipe sink run <my_sink_pipe> --param foo=bar",
)
@click.pass_context
@coro
async def pipe_sink_run(ctx: click.Context, pipe_name_or_id: str, wait: bool, yes: bool, param: Optional[Tuple[str]]):
    """Run an on-demand sink job"""

    params = dict(key_value.split("=") for key_value in param) if param else {}

    if yes or click.confirm(FeedbackManager.warning_confirm_sink_job(pipe=pipe_name_or_id)):
        click.echo(FeedbackManager.info_sink_job_running(pipe=pipe_name_or_id))
        client: TinyB = ctx.ensure_object(dict)["client"]

        try:
            pipe = await client.pipe(pipe_name_or_id)
            connections = await client.get_connections()

            current_sink = None
            for connection in connections:
                for sink in connection.get("sinks", []):
                    if sink.get("resource_id") == pipe["id"]:
                        current_sink = sink
                        break

            if not current_sink:
                raise Exception(f"Pipe {connections} does not have an associated connection")

            bucket_path = current_sink["settings"]["bucket_path"]
            response = await client.pipe_run_sink(pipe_name_or_id, params)
            job_id = response["job"]["id"]
            job_url = response["job"]["job_url"]
            click.echo(FeedbackManager.success_sink_job_created(bucket_path=bucket_path, job_id=job_id))

            if wait:
                await wait_job(client, job_id, job_url, "** Sinking data")
                click.echo(FeedbackManager.success_sink_job_finished(bucket_path=bucket_path))

        except Exception as e:
            raise CLIPipeException(FeedbackManager.error_creating_sink_job(error=str(e)))
