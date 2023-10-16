# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import os
from os import environ, getcwd

import difflib
import json
import logging
import pprint
import re
import shutil
import sys
import click
from click import Context

from pathlib import Path
from typing import Any, Iterable, Optional, List, Dict, Tuple

import humanfriendly
from toposort import toposort

from tinybird.client import AuthException, AuthNoTokenException, CanNotBeDeletedException, DoesNotExistException, TinyB
from tinybird.connectors import create_connector

from tinybird.feedback_manager import FeedbackManager
from tinybird.datafile import (
    AlreadyExistsException,
    Datafile,
    ParseException,
    build_graph,
    folder_push,
    folder_pull,
    format_datasource,
    format_pipe,
    get_name_tag_version,
    get_project_filenames,
    parse_datasource,
    parse_pipe,
    wait_job,
    get_resource_versions,
    diff_command,
    CLIGitRelease,
    CLIGitReleaseException,
    peek,
    color_diff,
    parse_token,
)
import tinybird.context as context
from tinybird.config import FeatureFlags, get_config, VERSION, CURRENT_VERSION, SUPPORTED_CONNECTORS

from tinybird.tb_cli_modules.common import (
    CLIException,
    CatchAuthExceptions,
    coro,
    create_tb_client,
    folder_init,
    get_current_main_workspace,
    getenv_bool,
    load_connector_config,
    get_config_and_hosts,
    echo_safe_humanfriendly_tables_format_smart_table,
)
from tinybird.tb_cli_modules.telemetry import add_telemetry_event
from tinybird.tb_cli_modules.cicd import init_cicd, check_cicd_exists

__old_click_echo = click.echo


@click.group(cls=CatchAuthExceptions, context_settings={"help_option_names": ["-h", "--help"]})  # noqa: C901
@click.option(
    "--debug/--no-debug",
    default=False,
    help="Prints internal representation, can be combined with any command to get more information.",
)
@click.option("--token", envvar="TB_TOKEN", help="Use auth token, defaults to TB_TOKEN envvar, then to the .tinyb file")
@click.option(
    "--host", envvar="TB_HOST", help="Use custom host, defaults to TB_HOST envvar, then to https://api.tinybird.co"
)
@click.option("--gcp-project-id", help="The Google Cloud project ID", hidden=True)
@click.option(
    "--gcs-bucket", help="The Google Cloud Storage bucket to write temp files when using the connectors", hidden=True
)
@click.option(
    "--google-application-credentials",
    envvar="GOOGLE_APPLICATION_CREDENTIALS",
    help="Set GOOGLE_APPLICATION_CREDENTIALS",
    hidden=True,
)
@click.option("--sf-account", help="The Snowflake Account (e.g. your-domain.west-europe.azure)", hidden=True)
@click.option("--sf-warehouse", help="The Snowflake warehouse name", hidden=True)
@click.option("--sf-database", help="The Snowflake database name", hidden=True)
@click.option("--sf-schema", help="The Snowflake schema name", hidden=True)
@click.option("--sf-role", help="The Snowflake role name", hidden=True)
@click.option("--sf-user", help="The Snowflake user name", hidden=True)
@click.option("--sf-password", help="The Snowflake password", hidden=True)
@click.option(
    "--sf-storage-integration",
    help="The Snowflake GCS storage integration name (leave empty to auto-generate one)",
    hidden=True,
)
@click.option("--sf-stage", help="The Snowflake GCS stage name (leave empty to auto-generate one)", hidden=True)
@click.option(
    "--with-headers", help="Flag to enable connector to export with headers", is_flag=True, default=False, hidden=True
)
@click.option(
    "--version-warning/--no-version-warning",
    envvar="TB_VERSION_WARNING",
    default=True,
    help="Don't print version warning message if there's a new available version. You can use TB_VERSION_WARNING envar",
)
@click.option(
    "--hide-tokens",
    is_flag=True,
    default=False,
    help="Disable the output of tokens [DEPRECATED: tokens are hidden by default]",
)
@click.option("--show-tokens", is_flag=True, default=False, help="Enable the output of tokens")
@click.version_option(version=VERSION)
@click.pass_context
@coro
async def cli(
    ctx: Context,
    debug: bool,
    token: str,
    host: str,
    gcp_project_id: str,
    gcs_bucket: str,
    google_application_credentials: str,
    sf_account: str,
    sf_warehouse: str,
    sf_database: str,
    sf_schema: str,
    sf_role: str,
    sf_user: str,
    sf_password: str,
    sf_storage_integration: str,
    sf_stage,
    with_headers: bool,
    version_warning: bool,
    hide_tokens: bool,
    show_tokens: bool,
) -> None:
    if hide_tokens:
        click.echo(
            FeedbackManager.warning_deprecated(
                warning="The `--hide-tokens` flag is deprecated. Tokens are hidden by default, see `tb --help` for more info."
            )
        )

    # We need to unpatch for our tests not to break
    if show_tokens:
        __unpatch_click_output()
    else:
        __patch_click_output()

    if getenv_bool("TB_DISABLE_SSL_CHECKS", False):
        click.echo(FeedbackManager.warning_disabled_ssl_checks())

    # ensure that ctx.obj exists and is a dict (in case `cli()` is called)
    # by means other than the `if` block below
    if not environ.get("PYTEST", None) and version_warning and not token:
        from tinybird.check_pypi import CheckPypi

        latest_version = await CheckPypi().get_latest_version()

        if "x.y.z" in CURRENT_VERSION:
            click.echo(FeedbackManager.warning_development_cli())

        if "x.y.z" not in CURRENT_VERSION and latest_version != CURRENT_VERSION:
            click.echo(FeedbackManager.warning_update_version(latest_version=latest_version))
            click.echo(FeedbackManager.warning_current_version(current_version=CURRENT_VERSION))

    if debug:
        logging.basicConfig(level=logging.DEBUG)

    config = await get_config(host, token)
    client = TinyB(config.get("token", None), config["host"], version=VERSION, send_telemetry=True)

    # If they have passed a token or host as paramter and it's different that record in .tinyb, refresh the workspace id
    if token or host:
        try:
            workspace = await client.workspace_info()
            config["id"] = workspace.get("id", "")
        # If we can not get this info, we continue with the id on the file
        except (AuthNoTokenException, AuthException):
            pass

    ctx.ensure_object(dict)["config"] = config

    if ctx.invoked_subcommand == "auth":
        return

    if gcp_project_id and gcs_bucket and google_application_credentials and not sf_account:
        bq_config = {
            "project_id": gcp_project_id,
            "bucket_name": gcs_bucket,
            "service_account": google_application_credentials,
            "with_headers": with_headers,
        }
        ctx.ensure_object(dict)["bigquery"] = create_connector("bigquery", bq_config)
    if (
        sf_account
        and sf_warehouse
        and sf_database
        and sf_schema
        and sf_role
        and sf_user
        and sf_password
        and gcs_bucket
        and google_application_credentials
        and gcp_project_id
    ):
        sf_config = {
            "account": sf_account,
            "warehouse": sf_warehouse,
            "database": sf_database,
            "schema": sf_schema,
            "role": sf_role,
            "user": sf_user,
            "password": sf_password,
            "storage_integration": sf_storage_integration,
            "stage": sf_stage,
            "bucket_name": gcs_bucket,
            "service_account": google_application_credentials,
            "project_id": gcp_project_id,
            "with_headers": with_headers,
        }
        ctx.ensure_object(dict)["snowflake"] = create_connector("snowflake", sf_config)

    logging.debug("debug enabled")

    ctx.ensure_object(dict)["client"] = client

    for connector in SUPPORTED_CONNECTORS:
        load_connector_config(ctx, connector, debug, check_uninstalled=True)


@cli.command()
@click.option(
    "--generate-datasources",
    is_flag=True,
    default=False,
    help="Generate datasources based on CSV, NDJSON and Parquet files in this folder",
)
@click.option(
    "--folder",
    default=None,
    type=click.Path(exists=True, file_okay=False),
    help="Folder where datafiles will be placed",
)
@click.option("-f", "--force", is_flag=True, default=False, help="Overrides existing files")
@click.option(
    "-ir",
    "--ignore-remote",
    is_flag=True,
    default=False,
    help="Ignores remote files not present in the local data project on git init",
)
@click.option(
    "--git",
    is_flag=True,
    default=False,
    help="Init workspace with git releases. Generates CI/CD files for yout git provider",
)
@click.option("--override-commit", default=None, help="Pass commit in case want to override git commit reference")
@click.pass_context
@coro
async def init(
    ctx: Context,
    generate_datasources: bool,
    folder: str,
    force: bool,
    ignore_remote: bool,
    git: bool,
    override_commit: str,
) -> None:
    """Initialize folder layout."""
    client: TinyB = ctx.ensure_object(dict)["client"]
    config, _, _ = await get_config_and_hosts(ctx, check_token_exists=True)
    folder = folder if folder else getcwd()

    workspaces: List[Dict[str, Any]] = (await client.user_workspaces_and_branches()).get("workspaces", [])
    current_ws: Dict[str, Any] = next(
        (workspace for workspace in workspaces if config and workspace.get("id", ".") == config.get("id", "..")), {}
    )

    if current_ws.get("is_branch"):
        click.echo(FeedbackManager.error_not_allowed_in_branch())
        return

    await folder_init(client, folder, generate_datasources, generate_releases=True, force=force)

    if git:
        cli_git_release = None
        try:
            cli_git_release = CLIGitRelease(path=folder)
        except CLIGitReleaseException:
            raise CLIGitReleaseException(FeedbackManager.error_no_git_repo_for_init(repo_path=folder))

        if not cli_git_release.is_dottinyb_ignored():
            raise CLIGitReleaseException(
                FeedbackManager.error_dottinyb_not_ignored(git_working_dir=f"{cli_git_release.working_dir()}/")
            )
        else:
            click.echo(FeedbackManager.info_dottinyb_already_ignored())

        if (
            os.path.exists(f"{cli_git_release.working_dir()}/.diff_tmp")
            and not cli_git_release.is_dotdifftemp_ignored()
        ):
            raise CLIGitReleaseException(
                FeedbackManager.error_dotdiff_not_ignored(git_working_dir=f"{cli_git_release.working_dir()}/")
            )
        else:
            click.echo(FeedbackManager.info_dotdifftemp_already_ignored())

        if "release" not in current_ws:
            raise CLIGitReleaseException(FeedbackManager.error_no_correct_token_for_init())

        elif current_ws.get("release") and not override_commit:
            final_response = FeedbackManager.error_release_already_set(
                workspace=current_ws["name"], commit=current_ws["release"]["commit"]
            )

        elif override_commit:
            if click.confirm(
                FeedbackManager.prompt_init_git_release_force(
                    current_commit=current_ws["release"]["commit"], new_commit=override_commit
                )
            ):
                try:
                    release = await cli_git_release.update_release(client, current_ws, override_commit)
                except Exception as exc:
                    raise CLIGitReleaseException(FeedbackManager.error_exception(error=str(exc)))

                final_response = FeedbackManager.success_init_git_release(
                    workspace_name=current_ws["name"], release_commit=release["commit"]
                )
            else:
                return

        else:
            click.echo(FeedbackManager.info_no_git_release_yet(workspace=current_ws["name"]))
            click.echo(FeedbackManager.info_diff_resources_for_git_init())
            changed = await diff_command(
                [], True, client, with_print=False, verbose=False, clean_up=True, progress_bar=True
            )
            changed = {
                k: v
                for k, v in changed.items()
                if v is not None and (not ignore_remote or v not in ["remote", "shared"])
            }
            if changed:
                tb_pull_command = "tb pull --force"
                click.echo(FeedbackManager.warning_git_release_init_with_diffs())
                if click.confirm(FeedbackManager.prompt_init_git_release_pull(pull_command=tb_pull_command)):
                    await folder_pull(client, folder, auto=True, match=None, prefix=None, force=True)

                else:
                    raise CLIGitReleaseException(
                        FeedbackManager.error_diff_resources_for_git_init(
                            workspace=current_ws["name"], pull_command=tb_pull_command
                        )
                    )
            else:
                click.echo(FeedbackManager.info_git_release_init_without_diffs(workspace=current_ws["name"]))
            if cli_git_release.is_dirty_to_init():
                raise CLIGitReleaseException(
                    FeedbackManager.error_commit_changes_to_init_release(
                        path=cli_git_release.path, git_output=cli_git_release.status()
                    )
                )
            try:
                release = await cli_git_release.update_release(client, current_ws)
            except Exception as exc:
                raise CLIGitReleaseException(FeedbackManager.error_exception(error=str(exc)))

            final_response = FeedbackManager.success_init_git_release(
                workspace_name=current_ws["name"], release_commit=release["commit"]
            )

        cicd_provider = await check_cicd_exists(cli_git_release.working_dir())
        if not force and cicd_provider:
            click.echo(FeedbackManager.info_cicd_already_exists(provider=cicd_provider.name))
        else:
            if click.confirm(FeedbackManager.prompt_init_cicd(), default=True):
                await init_cicd(client, current_ws, config, path=cli_git_release.working_dir())

        click.echo(final_response)

    return


@cli.command()
@click.argument("filenames", type=click.Path(exists=True), nargs=-1, default=None)
@click.option("--debug", is_flag=True, default=False, help="Print internal representation")
def check(filenames: List[str], debug: bool) -> None:
    """Check file syntax."""

    if not filenames:
        filenames = get_project_filenames(".")

    def process(filenames: Iterable):
        parser_matrix = {".pipe": parse_pipe, ".datasource": parse_datasource, ".token": parse_token}
        try:
            for filename in filenames:
                if os.path.isdir(filename):
                    process(filenames=get_project_filenames(filename))

                click.echo(FeedbackManager.info_processing_file(filename=filename))
                doc: Datafile
                parser = parser_matrix.get(Path(filename).suffix)
                if not parser:
                    raise ParseException(FeedbackManager.error_unsupported_datafile(extension=Path(filename).suffix))

                doc = parser(filename)

                click.echo(FeedbackManager.success_processing_file(filename=filename))
                if debug:
                    pp = pprint.PrettyPrinter()
                    for x in doc.nodes:
                        pp.pprint(x)

        except ParseException as e:
            raise CLIException(FeedbackManager.error_exception(error=e))

    process(filenames=filenames)


@cli.command()
@click.option("--prefix", default="", help="Use prefix for all the resources", hidden=True)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Run the command without creating resources on the Tinybird account or any side effect",
)
@click.option(
    "--check/--no-check", is_flag=True, default=True, help="Enable/Disable output checking, enabled by default"
)
@click.option("--push-deps", is_flag=True, default=False, help="Push dependencies, disabled by default")
@click.option(
    "--only-changes",
    is_flag=True,
    default=False,
    help="Push only the resources that have changed compared to the destination workspace",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Prints internal representation, can be combined with any command to get more information.",
)
@click.option("-f", "--force", is_flag=True, default=False, help="Override pipes when they already exist")
@click.option(
    "--override-datasource",
    is_flag=True,
    default=False,
    help="When pushing a pipe with a Materialized node if the target Data Source exists it will try to override it.",
)
@click.option("--populate", is_flag=True, default=False, help="Populate materialized nodes when pushing them")
@click.option(
    "--subset",
    type=float,
    default=None,
    help="Populate with a subset percent of the data (limited to a maximum of 2M rows), this is useful to quickly test a materialized node with some data. The subset must be greater than 0 and lower than 0.1. A subset of 0.1 means a 10 percent of the data in the source Data Source will be used to populate the materialized view. Use it together with --populate, it has precedence over --sql-condition",
)
@click.option(
    "--sql-condition",
    type=str,
    default=None,
    help="Populate with a SQL condition to be applied to the trigger Data Source of the Materialized View. For instance, `--sql-condition='date == toYYYYMM(now())'` it'll populate taking all the rows from the trigger Data Source which `date` is the current month. Use it together with --populate. --sql-condition is not taken into account if the --subset param is present. Including in the ``sql_condition`` any column present in the Data Source ``engine_sorting_key`` will make the populate job process less data.",
)
@click.option(
    "--unlink-on-populate-error",
    is_flag=True,
    default=False,
    help="If the populate job fails the Materialized View is unlinked and new data won't be ingested in the Materialized View. First time a populate job fails, the Materialized View is always unlinked.",
)
@click.option("--fixtures", is_flag=True, default=False, help="Append fixtures to data sources")
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="To be used along with --populate command. Waits for populate jobs to finish, showing a progress bar. Disabled by default.",
)
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
@click.option(
    "--only-response-times", is_flag=True, default=False, help="Checks only response times, when --force push a pipe"
)
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
@click.option("--timeout", type=float, default=None, help="timeout you want to use for the job populate")
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
@click.option(
    "--folder",
    default=".",
    help="Folder from where to execute the command. By default the current folder",
    hidden=True,
    type=click.types.STRING,
)
@click.option(
    "--user_token",
    is_flag=False,
    default=None,
    help="The user token is required for sharing a datasource that contains the SHARED_WITH entry.",
    type=click.types.STRING,
)
@click.option(
    "--is-internal",
    is_flag=True,
    default=False,
    help="Use when working with the Internal workspace as by default users can not create MV from internal datasources",
    hidden=True,
)
@click.pass_context
@coro
async def push(
    ctx: Context,
    prefix: str,
    filenames: Optional[List[str]],
    dry_run: bool,
    check: bool,
    push_deps: bool,
    only_changes: bool,
    debug: bool,
    force: bool,
    override_datasource: bool,
    populate: bool,
    subset: Optional[float],
    sql_condition: Optional[str],
    unlink_on_populate_error: bool,
    fixtures: bool,
    wait: bool,
    yes: bool,
    only_response_times: bool,
    workspace_map,
    workspace,
    no_versions: bool,
    timeout: Optional[float],
    limit: int,
    sample_by_params: int,
    failfast: bool,
    ignore_order: bool,
    validate_processed_bytes: bool,
    check_requests_from_main: bool,
    folder: str,
    user_token: Optional[str],
    is_internal: bool,
) -> None:
    """Push files to Tinybird."""

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
        dry_run,
        check,
        push_deps,
        only_changes,
        debug=debug,
        force=force,
        override_datasource=override_datasource,
        populate=populate,
        populate_subset=subset,
        populate_condition=sql_condition,
        unlink_on_populate_error=unlink_on_populate_error,
        upload_fixtures=fixtures,
        wait=wait,
        ignore_sql_errors=ignore_sql_errors,
        skip_confirmation=yes,
        only_response_times=only_response_times,
        workspace_map=dict(workspace_map),
        workspace_lib_paths=workspace,
        no_versions=no_versions,
        timeout=timeout,
        run_tests=False,
        tests_to_run=limit,
        tests_sample_by_params=sample_by_params,
        tests_failfast=failfast,
        tests_ignore_order=ignore_order,
        tests_validate_processed_bytes=validate_processed_bytes,
        tests_check_requests_from_branch=check_requests_from_main,
        folder=folder,
        config=ctx.ensure_object(dict)["config"],
        user_token=user_token,
        is_internal=is_internal,
    )
    return


@cli.command()  # noqa: C901
@click.option(
    "--folder", default=None, type=click.Path(exists=True, file_okay=False), help="Folder where files will be placed"
)
@click.option(
    "--auto/--no-auto",
    is_flag=True,
    default=True,
    help="Saves datafiles automatically into their default directories (/datasources or /pipes). Default is True",
)
@click.option("--match", default=None, help="Retrieve any resourcing matching the pattern. eg --match _test")
@click.option("--prefix", default=None, help="Download only resources with this prefix", hidden=True)
@click.option("-f", "--force", is_flag=True, default=False, help="Override existing files")
@click.pass_context
@coro
async def pull(
    ctx: Context,
    folder: str,
    auto: bool,
    match: Optional[str],
    prefix: Optional[str],
    force: bool,
) -> None:
    """Retrieve latest versions for project files from Tinybird."""

    if prefix:
        click.echo(
            FeedbackManager.warning_deprecated(
                warning="The `--prefix` flag is deprecated and EOL is planned for 20th of Dec. You should use different workspaces instead, see this migration guide for more info => https://www.tinybird.co/docs/guides/staging-and-production-workspaces.html#migrating-from-prefixes"
            )
        )

    client = ctx.ensure_object(dict)["client"]
    folder = folder if folder else getcwd()

    return await folder_pull(client, folder, auto, match, prefix, force)


@cli.command()
@click.option("--no-deps", is_flag=True, default=False, help="Print only data sources with no pipes using them")
@click.option("--match", default=None, help="Retrieve any resource matching the pattern")
@click.option("--pipe", default=None, help="Retrieve any resource used by pipe")
@click.option("--datasource", default=None, help="Retrieve resources depending on this Data Source")
@click.option(
    "--check-for-partial-replace",
    is_flag=True,
    default=False,
    help="Retrieve dependant Data Sources that will have their data replaced if a partial replace is executed in the Data Source selected",
)
@click.option("--recursive", is_flag=True, default=False, help="Calculate recursive dependencies")
@click.pass_context
@coro
async def dependencies(
    ctx: Context,
    no_deps: bool,
    match: Optional[str],
    pipe: Optional[str],
    datasource: Optional[str],
    check_for_partial_replace: bool,
    recursive: bool,
) -> None:
    """Print all data sources dependencies."""

    client = ctx.ensure_object(dict)["client"]

    response = await client.datasource_dependencies(
        no_deps, match, pipe, datasource, check_for_partial_replace, recursive
    )
    for ds in response["dependencies"]:
        click.echo(FeedbackManager.info_dependency_list(dependency=ds))
        for pipe in response["dependencies"][ds]:
            click.echo(FeedbackManager.info_dependency_list_item(dependency=pipe))
    if "incompatible_datasources" in response and len(response["incompatible_datasources"]):
        click.echo(FeedbackManager.info_no_compatible_dependencies_found())
        for ds in response["incompatible_datasources"]:
            click.echo(FeedbackManager.info_dependency_list(dependency=ds))
        raise CLIException(FeedbackManager.error_partial_replace_cant_be_executed(datasource=datasource))


@cli.command()
@click.argument("filenames", type=click.Path(exists=True), nargs=-1, required=True)
@click.option(
    "--line-length",
    is_flag=False,
    default=100,
    help="A number indicating the maximum characters per line in the node SQL, lines will be splitted based on the SQL syntax and the number of characters passed as a parameter",
)
@click.option("--dry-run", is_flag=True, default=False, help="Don't ask to override the local file")
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation to overwrite the local file")
@click.option(
    "--diff",
    is_flag=True,
    default=False,
    help="Formats local file, prints the diff and exits 1 if different, 0 if equal",
)
@click.pass_context
@coro
async def fmt(
    ctx: Context, filenames: List[str], line_length: int, dry_run: bool, yes: bool, diff: bool
) -> Optional[str]:
    """
    Formats a .datasource, .pipe or .incl file

    This command removes comments starting with # from the file, use DESCRIPTION instead.

    The format command tries to parse the datafile so syntax errors might rise.

    .incl files must contain a NODE definition
    """

    result = ""
    for filename in filenames:
        if not diff:
            click.echo(filename)
        extension = Path(filename).suffix
        if extension == ".datasource":
            result = await format_datasource(filename)
        elif extension in [".pipe", ".incl"]:
            result = await format_pipe(filename, line_length)
        else:
            click.echo("Unsupported file type")
            return None

        if diff:
            result = result.rstrip("\n")
            lines_fmt = [f"{line}\n" for line in result.split("\n")]
            with open(filename, "r") as file:
                lines_file = file.readlines()
            diff_result = difflib.unified_diff(
                lines_file, lines_fmt, fromfile=f"{Path(filename).name} local", tofile="fmt datafile"
            )
            diff_result = color_diff(diff_result)
            not_empty, diff_lines = peek(diff_result)
            if not_empty:
                sys.stdout.writelines(diff_lines)
                click.echo("")
                sys.exit(1)
        else:
            click.echo(result)
            if dry_run:
                return None

            if yes or click.confirm(FeedbackManager.prompt_override_local_file(name=filename)):
                with open(f"{filename}", "w") as file:
                    file.write(result)

                click.echo(FeedbackManager.success_generated_local_file(file=filename))

    return result


@cli.command(
    name="diff",
    short_help="Diffs local datafiles to the corresponding remote files in the workspace. For the case of .datasource files it just diffs VERSION and SCHEMA, since ENGINE, KAFKA or other metadata is considered immutable.",
)
@click.argument("filename", type=click.Path(exists=True), nargs=-1, required=False)
@click.option(
    "--fmt/--no-fmt",
    is_flag=True,
    default=True,
    help="Format files before doing the diff, default is True so both files match the format",
)
@click.option("--no-color", is_flag=True, default=False, help="Don't colorize diff")
@click.option(
    "--no-verbose", is_flag=True, default=False, help="List the resources changed not the content of the diff"
)
@click.option(
    "--main",
    is_flag=True,
    default=False,
    help="Diffs local datafiles to the corresponding remote files in the main workspace. Only works when authenticated on an Environment.",
    hidden=True,
)
@click.option(
    "--production",
    is_flag=True,
    default=False,
    help="Diffs local datafiles to the corresponding remote files in the main workspace. Only works when authenticated on an Environment. (deprecated)",
    hidden=True,
)
@click.pass_context
@coro
async def diff(
    ctx: Context, filename: Optional[Tuple], fmt: bool, no_color: bool, no_verbose: bool, main: bool, production: bool
) -> None:
    only_resources_changed = no_verbose
    client: TinyB = ctx.ensure_object(dict)["client"]

    if production:
        click.echo(FeedbackManager.warning_deprecated(warning="--production flag is deprecated, use --main instead"))

    main = main or production
    if not main:
        changed = await diff_command(
            list(filename) if filename else None, fmt, client, no_color, with_print=not only_resources_changed
        )
    else:
        config, _, _ = await get_config_and_hosts(ctx)

        response = await client.user_workspaces_and_branches()
        ws_client = None
        for workspace in response["workspaces"]:
            if config["id"] == workspace["id"]:
                if not workspace.get("is_branch"):
                    click.echo(FeedbackManager.error_not_a_branch())
                    return

                origin = workspace["main"]
                workspace = await get_current_main_workspace(client, config)

                if not workspace:
                    click.echo(FeedbackManager.error_workspace(workspace=origin))
                    return

                ws_client = TinyB(workspace["token"], config["host"], version=VERSION, send_telemetry=True)
                break

        if not ws_client:
            click.echo(FeedbackManager.error_workspace(workspace=origin))
            return
        changed = await diff_command(
            list(filename) if filename else None, fmt, ws_client, no_color, with_print=not only_resources_changed
        )

    if only_resources_changed:
        click.echo("\n")
        for resource, status in dict(sorted(changed.items(), key=lambda item: str(item[1]))).items():
            if status is None:
                continue
            status = "changed" if status not in ["remote", "local", "shared"] else status
            click.echo(f"{status}: {resource}")


@cli.command()
@click.argument("query", required=False)
@click.option("--rows_limit", default=100, help="Max number of rows retrieved")
@click.option("--pipeline", default=None, help="The name of the Pipe to run the SQL Query")
@click.option("--pipe", default=None, help="The path to the .pipe file to run the SQL Query of a specific NODE")
@click.option("--node", default=None, help="The NODE name")
@click.option(
    "--format",
    "format_",
    type=click.Choice(["json", "csv", "human"], case_sensitive=False),
    default="human",
    help="Output format",
)
@click.option(
    "--semver",
    is_flag=False,
    required=False,
    type=str,
    help="Semver of a preview Release to run the query. Example: 1.0.0",
    hidden=True,
)
@click.option("--stats/--no-stats", default=False, help="Show query stats")
@click.pass_context
@coro
async def sql(
    ctx: Context,
    query: str,
    rows_limit: int,
    pipeline: Optional[str],
    pipe: Optional[str],
    node: Optional[str],
    format_: str,
    semver: Optional[str],
    stats: bool,
) -> None:
    """Run SQL query over data sources and pipes."""

    client = ctx.ensure_object(dict)["client"]
    req_format = "CSVWithNames" if format_ == "csv" else "JSON"
    try:
        if query:
            q = query.lower().strip()
            if q.startswith("insert"):
                click.echo(FeedbackManager.error_invalid_query())
                click.echo(FeedbackManager.info_append_data())
                return
            if q.startswith("delete"):
                click.echo(FeedbackManager.error_invalid_query())
                return
            res = await client.query(
                f"SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT {req_format}", pipeline=pipeline, semver=semver
            )
        elif pipe and node:
            datasources: List[Dict[str, Any]] = await client.datasources()
            pipes: List[Dict[str, Any]] = await client.pipes()

            existing_resources: List[str] = [x["name"] for x in datasources] + [x["name"] for x in pipes]
            resource_versions = get_resource_versions(existing_resources)

            filenames = [pipe]

            # build graph to get new versions for all the files involved in the query
            # dependencies need to be processed always to get the versions
            resources, dep_map = await build_graph(
                filenames,
                client,
                dir_path=".",
                tag=None,
                process_dependencies=True,
                skip_connectors=True,
            )

            # update existing versions
            latest_datasource_versions = resource_versions.copy()

            for dep in resources.values():
                ds = dep["resource_name"]
                if dep["version"] is not None:
                    latest_datasource_versions[ds] = dep["version"]

            # build the graph again with the rigth version
            to_run, _ = await build_graph(
                filenames,
                client,
                dir_path=".",
                tag=None,
                resource_versions=latest_datasource_versions,
                verbose=False,
            )
            query = ""
            for key in to_run:
                elem = to_run[key]
                for _node in elem["nodes"]:
                    if _node["params"]["name"].lower() == node.lower():
                        query = "".join(_node["sql"])
            pipeline = pipe.split("/")[-1].split(".pipe")[0]
            res = await client.query(
                f"SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT {req_format}", pipeline=pipeline, semver=semver
            )
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return

    if "error" in res:
        click.echo(FeedbackManager.error_exception(error=res["error"]))
        return

    if stats:
        stats_query = f"SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT JSON"
        stats_res = await client.query(stats_query, pipeline=pipeline)
        stats_dict = stats_res["statistics"]
        seconds = stats_dict["elapsed"]
        rows_read = humanfriendly.format_number(stats_dict["rows_read"])
        bytes_read = humanfriendly.format_size(stats_dict["bytes_read"])
        click.echo(FeedbackManager.info_query_stats(seconds=seconds, rows=rows_read, bytes=bytes_read))

    if format_ == "csv":
        click.echo(res)
    elif "data" in res and res["data"]:
        if format_ == "json":
            click.echo(json.dumps(res, indent=8))
        else:
            dd = []
            for d in res["data"]:
                dd.append(d.values())
            echo_safe_humanfriendly_tables_format_smart_table(dd, column_names=res["data"][0].keys())
    else:
        click.echo(FeedbackManager.info_no_rows())


@cli.command(
    name="materialize",
    short_help="Given a local Pipe datafile (.pipe) and a node name it generates the target Data Source and materialized Pipe ready to be pushed and guides you through the process to create the materialized view",
)
@click.argument("filename", type=click.Path(exists=True))
@click.argument("target_datasource", default=None, required=False)
@click.option("--prefix", default="", help="Use prefix for all the resources", hidden=True)
@click.option("--push-deps", is_flag=True, default=False, help="Push dependencies, disabled by default")
@click.option("--workspace_map", nargs=2, type=str, multiple=True, hidden=True)
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
@click.option("--verbose", is_flag=True, default=False, help="Prints more log")
@click.option("--force-populate", default=None, required=False, help="subset or full", hidden=True)
@click.option(
    "--unlink-on-populate-error",
    is_flag=True,
    default=False,
    help="If the populate job fails the Materialized View is unlinked and new data won't be ingested in the Materialized View. First time a populate job fails, the Materialized View is always unlinked.",
)
@click.option("--override-pipe", is_flag=True, default=False, help="Override pipe if exists or prompt", hidden=True)
@click.option(
    "--override-datasource", is_flag=True, default=False, help="Override data source if exists or prompt", hidden=True
)
@click.pass_context
@coro
async def materialize(
    ctx: Context,
    filename: str,
    prefix: str,
    push_deps: bool,
    workspace_map: List[str],
    workspace: List[str],
    no_versions: bool,
    verbose: bool,
    force_populate: Optional[str],
    unlink_on_populate_error: bool,
    override_pipe: bool,
    override_datasource: bool,
    target_datasource: Optional[str] = None,
) -> None:
    """[BETA] Given a local Pipe datafile path (FILENAME) and optionally a Materialized View name (TARGET_DATASOURCE), choose one of its nodes to materialize.

    This command guides you to generate the Materialized View with name TARGET_DATASOURCE, the only requirement is having a valid Pipe datafile locally. Use `tb pull` to download resources from your workspace when needed.

    Syntax: tb materialize path/to/pipe.pipe
    """
    if prefix:
        click.echo(
            FeedbackManager.warning_deprecated(
                warning="The `--prefix` flag is deprecated and EOL is planned for 20th of Dec. You should use different workspaces instead, see this migration guide for more info => https://www.tinybird.co/docs/guides/staging-and-production-workspaces.html#migrating-from-prefixes"
            )
        )

    cl = create_tb_client(ctx)

    async def _try_push_pipe_to_analyze(pipe_name):
        try:
            to_run = await folder_push(
                cl,
                tag=prefix,
                filenames=[filename],
                dry_run=False,
                check=False,
                push_deps=push_deps,
                debug=False,
                force=False,
                workspace_map=dict(workspace_map),
                workspace_lib_paths=workspace,
                no_versions=no_versions,
                run_tests=False,
                as_standard=True,
                raise_on_exists=True,
                verbose=verbose,
            )
        except AlreadyExistsException as e:
            if "Datasource" in str(e):
                click.echo(str(e))
                return
            if override_pipe or click.confirm(FeedbackManager.info_pipe_exists(name=pipe_name)):
                to_run = await folder_push(
                    cl,
                    tag=prefix,
                    filenames=[filename],
                    dry_run=False,
                    check=False,
                    push_deps=push_deps,
                    debug=False,
                    force=True,
                    workspace_map=dict(workspace_map),
                    workspace_lib_paths=workspace,
                    no_versions=no_versions,
                    run_tests=False,
                    as_standard=True,
                    verbose=verbose,
                )
            else:
                return
        except click.ClickException as ex:
            # HACK: By now, datafile raises click.ClickException instead of
            # CLIException to avoid circular imports. Thats we need to trace
            # the error here.
            #
            # Once we do a big refactor in datafile, we can get rid of this
            # snippet.
            msg: str = str(ex)
            add_telemetry_event("datafile_error", error=msg)
            click.echo(msg)

        return to_run

    def _choose_node_name(pipe):
        node = pipe["nodes"][0]
        materialized_nodes = [node for node in pipe["nodes"] if node["type"].lower() == "materialized"]

        if len(materialized_nodes) == 1:
            node = materialized_nodes[0]

        if len(pipe["nodes"]) > 1 and len(materialized_nodes) != 1:
            for index, node in enumerate(pipe["nodes"], start=1):
                click.echo(f"  [{index}] Materialize node with name => {node['name']}")
            option = click.prompt(FeedbackManager.prompt_choose_node(), default=len(pipe["nodes"]))
            node = pipe["nodes"][option - 1]
        node_name = node["name"]
        return node, node_name

    def _choose_target_datasource_name(pipe, node, node_name):
        datasource_name = target_datasource or node.get("datasource", None) or f'mv_{pipe["resource_name"]}_{node_name}'
        if prefix:
            datasource_name = "".join(datasource_name.split(f"{prefix}__")[1:])
        return datasource_name

    def _save_local_backup_pipe(pipe):
        pipe_bak = f"{filename}_bak"
        shutil.copyfile(filename, pipe_bak)
        pipe_file_name = f"{pipe['resource_name']}.pipe"
        if prefix:
            pipe_file_name = "".join(pipe_file_name.split(f"{prefix}__")[1:])

        click.echo(FeedbackManager.info_pipe_backup_created(name=pipe_bak))
        return pipe_file_name

    def _save_local_datasource(datasource_name, ds_datafile):
        base = Path("datasources")
        if not base.exists():
            base = Path()
        file_name = f"{datasource_name}.datasource"
        f = base / file_name
        with open(f"{f}", "w") as file:
            file.write(ds_datafile)

        click.echo(FeedbackManager.success_generated_local_file(file=f))
        return f

    async def _try_push_datasource(datasource_name, f):
        exists = False
        try:
            exists = await cl.get_datasource(datasource_name)
        except Exception:
            pass

        if exists:
            click.echo(FeedbackManager.info_materialize_push_datasource_exists(name=f.name))
            if override_datasource or click.confirm(FeedbackManager.info_materialize_push_datasource_override(name=f)):
                try:
                    await cl.datasource_delete(datasource_name, force=True)
                except DoesNotExistException:
                    pass

        filename = str(f.absolute())
        to_run = await folder_push(
            cl,
            tag=prefix,
            filenames=[filename],
            push_deps=push_deps,
            workspace_map=dict(workspace_map),
            workspace_lib_paths=workspace,
            no_versions=no_versions,
            verbose=verbose,
        )
        return to_run

    def _save_local_pipe(pipe_file_name, pipe_datafile, pipe):
        base = Path("pipes")
        if not base.exists():
            base = Path()
        f_pipe = base / pipe_file_name

        with open(f"{f_pipe}", "w") as file:
            if pipe["version"] is not None and pipe["version"] >= 0:
                pipe_datafile = f"VERSION {pipe['version']} \n {pipe_datafile}"
            prefix_name = ""
            if prefix:
                prefix_name = prefix
            matches = re.findall(rf"(({prefix_name}__)?([^\s\.]*)__v\d+)", pipe_datafile)
            for match in set(matches):
                if match[2] in pipe_datafile:
                    pipe_datafile = pipe_datafile.replace(match[0], match[2])
            file.write(pipe_datafile)

        click.echo(FeedbackManager.success_generated_local_file(file=f_pipe))
        return f_pipe

    async def _try_push_pipe(f_pipe):
        if override_pipe:
            option = 2
        else:
            click.echo(FeedbackManager.info_materialize_push_pipe_skip(name=f_pipe.name))
            click.echo(FeedbackManager.info_materialize_push_pipe_override(name=f_pipe.name))
            option = click.prompt(FeedbackManager.prompt_choose(), default=1)
        force = True
        check = True if option == 1 else False

        filename = str(f_pipe.absolute())
        to_run = await folder_push(
            cl,
            tag=prefix,
            filenames=[filename],
            dry_run=False,
            check=check,
            push_deps=push_deps,
            debug=False,
            force=force,
            unlink_on_populate_error=unlink_on_populate_error,
            workspace_map=dict(workspace_map),
            workspace_lib_paths=workspace,
            no_versions=no_versions,
            run_tests=False,
            verbose=verbose,
        )
        return to_run

    async def _populate(pipe, node_name, f_pipe):
        if force_populate or click.confirm(FeedbackManager.prompt_populate(file=f_pipe)):
            if not force_populate:
                click.echo(FeedbackManager.info_materialize_populate_partial())
                click.echo(FeedbackManager.info_materialize_populate_full())
                option = click.prompt(FeedbackManager.prompt_choose(), default=1)
            else:
                option = 1 if force_populate == "subset" else 2
            populate = False
            populate_subset = False
            if option == 1:
                populate_subset = 0.1
                populate = True
            elif option == 2:
                populate = True

            if populate:
                response = await cl.populate_node(
                    pipe["name"],
                    node_name,
                    populate_subset=populate_subset,
                    unlink_on_populate_error=unlink_on_populate_error,
                )
                if "job" not in response:
                    raise CLIException(response)

                job_url = response.get("job", {}).get("job_url", None)
                job_id = response.get("job", {}).get("job_id", None)
                click.echo(FeedbackManager.info_populate_job_url(url=job_url))
                wait_populate = True
                if wait_populate:
                    await wait_job(cl, job_id, job_url, "Populating")

    click.echo(FeedbackManager.warning_beta_tester())
    pipe_name = os.path.basename(filename).rsplit(".", 1)[0]
    if prefix:
        pipe_name = f"{prefix}__{pipe_name}"
    click.echo(FeedbackManager.info_before_push_materialize(name=filename))
    try:
        # extracted the materialize logic to local functions so the workflow is more readable
        to_run = await _try_push_pipe_to_analyze(pipe_name)

        if to_run is None:
            return

        pipe = to_run[pipe_name.split("/")[-1]]
        node, node_name = _choose_node_name(pipe)
        datasource_name = _choose_target_datasource_name(pipe, node, node_name)

        click.echo(FeedbackManager.info_before_materialize(name=pipe["name"]))
        analysis = await cl.analyze_pipe_node(pipe["name"], node, datasource_name=datasource_name)
        ds_datafile = analysis["analysis"]["datasource"]["datafile"]
        pipe_datafile = analysis["analysis"]["pipe"]["datafile"]

        pipe_file_name = _save_local_backup_pipe(pipe)
        f = _save_local_datasource(datasource_name, ds_datafile)
        await _try_push_datasource(datasource_name, f)

        f_pipe = _save_local_pipe(pipe_file_name, pipe_datafile, pipe)
        await _try_push_pipe(f_pipe)
        await _populate(pipe, node_name, f_pipe)

        prefix_name = f"{prefix}__" if prefix else ""
        click.echo(FeedbackManager.success_created_matview(name=f"{prefix_name}{datasource_name}"))
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))


@cli.command(
    short_help="Drop all the resources inside a project with prefix. This command is dangerous because it removes everything, use with care",
    hidden=True,
)  # noqa: C901
@click.argument("prefix")
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
@click.option("--dry-run", is_flag=True, default=False, help="Run the command without removing anything")
@click.pass_context
@coro
async def drop_prefix(ctx: Context, prefix: str, yes: bool, dry_run: bool) -> None:
    """Drop all the resources inside a project with prefix. This command is dangerous because it removes everything, use with care"""
    if prefix:
        click.echo(
            FeedbackManager.warning_deprecated(
                warning="This command is deprecated and EOL is planned for 20th of Dec. You should use different workspaces instead, see this migration guide for more info => https://www.tinybird.co/docs/guides/staging-and-production-workspaces.html#migrating-from-prefixes"
            )
        )

    if yes or click.confirm(FeedbackManager.warning_confirm_drop_prefix(prefix=prefix)):
        filenames = get_project_filenames(getcwd())
        context.disable_template_security_validation.set(True)
        resources, dep_map = await build_graph(filenames, create_tb_client(ctx), process_dependencies=True)
        names = [r["resource_name"].replace(".", "_") for r in resources.values()]
        res = {}
        client = ctx.ensure_object(dict)["client"]

        pipes = await client.pipes()
        for pipe in pipes:
            tk = get_name_tag_version(pipe["name"], ignore_prefix=False)
            if tk["tag"] == prefix and tk["name"] in names:
                res[tk["name"]] = pipe["name"]

        for group in reversed(list(toposort(dep_map))):
            for name in group:
                if name in res:
                    if resources[name]["resource"] == "datasources":
                        if not dry_run:
                            click.echo(FeedbackManager.info_removing_datasource(datasource=res[name]))
                            try:
                                await client.datasource_delete(res[name], force=True)
                            except DoesNotExistException:
                                click.echo(FeedbackManager.info_removing_datasource_not_found(datasource=res[name]))
                            except CanNotBeDeletedException as e:
                                click.echo(
                                    FeedbackManager.error_datasource_can_not_be_deleted(datasource=res[name], error=e)
                                )
                            except Exception as e:
                                raise CLIException(FeedbackManager.error_exception(error=e))
                        else:
                            click.echo(FeedbackManager.info_dry_removing_datasource(datasource=res[name]))
                    else:
                        if not dry_run:
                            click.echo(FeedbackManager.info_removing_pipe(pipe=res[name]))
                            try:
                                await client.pipe_delete(res[name])
                            except DoesNotExistException:
                                click.echo(FeedbackManager.info_removing_pipe_not_found(pipe=res[name]))
                        else:
                            click.echo(FeedbackManager.info_dry_removing_pipe(pipe=res[name]))

        ds = await client.datasources()
        for t in ds:
            tk = get_name_tag_version(t["name"], ignore_prefix=False)
            if tk["tag"] == prefix and tk["name"] in names:
                res[tk["name"]] = t["name"]
                if not dry_run:
                    click.echo(FeedbackManager.info_removing_datasource(datasource=t["name"]))
                    try:
                        await client.datasource_delete(t["name"], force=True)
                    except DoesNotExistException:
                        click.echo(FeedbackManager.info_removing_datasource_not_found(datasource=t["name"]))
                    except CanNotBeDeletedException as e:
                        click.echo(FeedbackManager.error_datasource_can_not_be_deleted(datasource=t["name"], error=e))
                    except Exception as e:
                        raise CLIException(FeedbackManager.error_exception(error=e))
                else:
                    click.echo(FeedbackManager.info_dry_removing_datasource(datasource=t["name"]))


def __patch_click_output():
    import re

    __old_click_echo = click.echo

    def obfuscate(msg: Any, *args, **kwargs) -> None:
        msg = re.sub(r"p\.ey[A-Za-z0-9-_\.]+", "p.ey****...****", str(msg))
        __old_click_echo(msg, *args, **kwargs)

    click.echo = obfuscate


def __unpatch_click_output():
    click.echo = __old_click_echo


@cli.command(short_help="Learn how to include info about the CLI in your shell PROMPT")  # noqa: C901
@click.pass_context
@coro
async def prompt(_ctx: Context) -> None:
    click.secho("Follow these instructions => https://www.tinybird.co/docs/cli.html#configure-the-shell-prompt")


@cli.command()
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Run the command without creating resources on the Tinybird account or any side effect",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Prints internal representation, can be combined with any command to get more information.",
)
@click.option("-f", "--force", is_flag=True, default=False, help="Override pipes when they already exist")
@click.option(
    "--override-datasource",
    is_flag=True,
    default=False,
    help="When pushing a pipe with a Materialized node if the target Data Source exists it will try to override it.",
)
@click.option("--populate", is_flag=True, default=False, help="Populate materialized nodes when pushing them")
@click.option(
    "--subset",
    type=float,
    default=None,
    help="Populate with a subset percent of the data (limited to a maximum of 2M rows), this is useful to quickly test a materialized node with some data. The subset must be greater than 0 and lower than 0.1. A subset of 0.1 means a 10 percent of the data in the source Data Source will be used to populate the materialized view. Use it together with --populate, it has precedence over --sql-condition",
)
@click.option(
    "--sql-condition",
    type=str,
    default=None,
    help="Populate with a SQL condition to be applied to the trigger Data Source of the Materialized View. For instance, `--sql-condition='date == toYYYYMM(now())'` it'll populate taking all the rows from the trigger Data Source which `date` is the current month. Use it together with --populate. --sql-condition is not taken into account if the --subset param is present. Including in the ``sql_condition`` any column present in the Data Source ``engine_sorting_key`` will make the populate job process less data.",
)
@click.option(
    "--unlink-on-populate-error",
    is_flag=True,
    default=False,
    help="If the populate job fails the Materialized View is unlinked and new data won't be ingested in the Materialized View. First time a populate job fails, the Materialized View is always unlinked.",
)
@click.option("--fixtures", is_flag=True, default=False, help="Append fixtures to data sources")
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="To be used along with --populate command. Waits for populate jobs to finish, showing a progress bar. Disabled by default.",
)
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
@click.option("--workspace_map", nargs=2, type=str, multiple=True)
@click.option(
    "--workspace",
    nargs=2,
    type=str,
    multiple=True,
    help="add a workspace path to the list of external workspaces, usage: --workspace name path/to/folder",
)
@click.option("--timeout", type=float, default=None, help="timeout you want to use for the job populate")
@click.option(
    "--folder",
    default=".",
    help="Folder from where to execute the command. By default the current folder",
    hidden=True,
    type=click.types.STRING,
)
@click.option(
    "--user_token",
    is_flag=False,
    default=None,
    help="The user token is required for sharing a datasource that contains the SHARED_WITH entry.",
    type=click.types.STRING,
)
@click.option(
    "--fork-downstream",
    is_flag=True,
    default=False,
    help="Creates new versions of the dependent downstream resources to the changed resources.",
    hidden=True,
)
@click.option(
    "--is-internal",
    is_flag=True,
    default=False,
    help="Use when working with the Internal workspace as by default users can not create MV from internal datasources",
    hidden=True,
)
@click.pass_context
@coro
async def deploy(
    ctx: Context,
    dry_run: bool,
    debug: bool,
    force: bool,
    override_datasource: bool,
    populate: bool,
    subset: Optional[float],
    sql_condition: Optional[str],
    unlink_on_populate_error: bool,
    fixtures: bool,
    wait: bool,
    yes: bool,
    workspace_map,
    workspace,
    timeout: Optional[float],
    folder: str,
    user_token: Optional[str],
    fork_downstream: bool,
    is_internal: bool,
) -> None:
    """Deploy in tinybird pushing resources changed from previous release using git"""

    ignore_sql_errors = FeatureFlags.ignore_sql_errors()
    context.disable_template_security_validation.set(True)
    await folder_push(
        tb_client=create_tb_client(ctx),
        dry_run=dry_run,
        check=False,
        push_deps=True,
        debug=debug,
        force=True,
        git_release=True,
        only_changes=False,
        override_datasource=override_datasource,
        populate=populate,
        populate_subset=subset,
        populate_condition=sql_condition,
        unlink_on_populate_error=unlink_on_populate_error,
        upload_fixtures=fixtures,
        wait=wait,
        ignore_sql_errors=ignore_sql_errors,
        skip_confirmation=yes,
        workspace_map=dict(workspace_map),
        workspace_lib_paths=workspace,
        timeout=timeout,
        run_tests=False,
        folder=folder,
        config=ctx.ensure_object(dict)["config"],
        user_token=user_token,
        fork_downstream=fork_downstream,
        is_internal=is_internal,
    )
    return
