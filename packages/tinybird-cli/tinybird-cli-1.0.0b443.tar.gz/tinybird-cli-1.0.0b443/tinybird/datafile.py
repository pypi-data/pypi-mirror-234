"""
Datafile is like a Dockerfile but to describe ETL processes
"""
try:
    from colorama import Fore, Back, Style, init

    init()
except ImportError:  # fallback so that the imported classes always exist

    class ColorFallback:
        def __getattr__(self, name):
            return ""

    Fore = Back = Style = ColorFallback()

import os
import itertools
from os import getcwd
import logging
import asyncio
import textwrap
import json
from operator import itemgetter
import shlex
import sys
import re
from typing import Any, Callable, Dict, Generator, Iterable, List, Optional, Tuple, Union, cast, Set
from enum import Enum
from mypy_extensions import VarArg, KwArg
import difflib
import click
import glob
import pprint
import requests
import unittest
from string import Template
from toposort import toposort
from pathlib import Path
import urllib.parse
from urllib.parse import urlencode, urlparse, parse_qs
from collections import namedtuple
from io import StringIO
import os.path
from copy import deepcopy
import traceback
from dataclasses import dataclass
from croniter import croniter
from click._termui_impl import ProgressBar
from contextlib import nullcontext

import shutil

from .tornado_template import UnClosedIfError
from .sql import parse_table_structure, schema_to_sql_columns
from .client import JobException, TinyB, DoesNotExistException
from .sql_template import render_sql_template, get_used_tables_in_template
from tinybird.sql_template_fmt import format_sql_template
from .feedback_manager import FeedbackManager
from .ch_utils.engine import ENABLED_ENGINES
from tinybird.syncasync import sync_to_async
from tinybird.config import VERSION, PROJECT_PATHS
from statistics import mean, median
import math
from humanfriendly.tables import format_pretty_table
from humanfriendly import format_size
from tinybird.tb_cli_modules.exceptions import CLIPipeException, CLIGitReleaseException

os.environ["GIT_PYTHON_REFRESH"] = "quiet"
from git import Repo, HEAD, Diff, InvalidGitRepositoryError, GitCommandError  # noqa: E402


INTERNAL_TABLES: Tuple[str, ...] = (
    "datasources_ops_log",
    "snapshot_views",
    "pipe_stats",
    "pipe_stats_rt",
    "block_log",
    "data_connectors_log",
    "kafka_ops_log",
    "datasources_storage",
)


PIPE_CHECKER_RETRIES: int = 3


class PipeTypes:
    MATERIALIZED = "materialized"
    ENDPOINT = "endpoint"
    COPY = "copy"
    DATA_SINK = "sink"
    DEFAULT = "default"


class PipeNodeTypes:
    MATERIALIZED = "materialized"
    ENDPOINT = "endpoint"
    STANDARD = "standard"
    DEFAULT = "default"
    DATA_SINK = "sink"
    COPY = "copy"


class DataFileExtensions:
    PIPE = ".pipe"
    DATASOURCE = ".datasource"
    INCL = ".incl"
    TOKEN = ".token"


class ImportReplacements:
    _REPLACEMENTS: Tuple[Tuple[str, str, Optional[str]], ...] = (
        ("import_service", "service", None),
        ("import_strategy", "mode", "replace"),
        ("import_connection_name", "connection", None),
        ("import_schedule", "cron", "@on-demand"),
        ("import_query", "query", None),
        ("import_connector", "connector", None),
        ("import_external_datasource", "external_data_source", None),
        ("import_bucket_uri", "bucket_uri", None),
    )

    @staticmethod
    def get_datafile_parameter_keys() -> List[str]:
        return [x[0] for x in ImportReplacements._REPLACEMENTS]

    @staticmethod
    def get_api_param_for_datafile_param(connector_service: str, key: str) -> Tuple[Optional[str], Optional[str]]:
        """Returns the API parameter name and default value for a given
        datafile parameter.
        """
        key = key.lower()
        for datafile_k, linker_k, value in ImportReplacements._REPLACEMENTS:
            if datafile_k == key:
                return linker_k, value
        return None, None

    @staticmethod
    def get_datafile_param_for_linker_param(connector_service: str, linker_param: str) -> Optional[str]:
        """Returns the datafile parameter name for a given linter parameter."""
        linker_param = linker_param.lower()
        for datafile_k, linker_k, _ in ImportReplacements._REPLACEMENTS:
            if linker_k == linker_param:
                return datafile_k
        return None

    @staticmethod
    def get_datafile_value_for_linker_value(
        connector_service: str, linker_param: str, linker_value: str
    ) -> Optional[str]:
        """Map linker values to datafile values."""
        linker_param = linker_param.lower()
        if linker_param != "cron":
            return linker_value
        if linker_value == "@once":
            return "@on-demand"
        if connector_service == "s3":
            return "@auto"
        return linker_value


class ExportReplacements:
    SERVICES = ("gcs_hmac", "s3")
    NODE_TYPES = PipeNodeTypes.DATA_SINK
    _REPLACEMENTS = (
        ("export_service", "service", None),
        ("export_connection_name", "connection", None),
        ("export_schedule", "schedule_cron", ""),
        ("export_bucket_uri", "path", None),
        ("export_file_template", "file_template", None),
        ("export_format", "format", "csv"),
        ("export_compression", "compression", None),
        ("export_strategy", "strategy", "@new"),
    )

    @staticmethod
    def is_export_node(node: Dict[str, Optional[str]]) -> bool:
        export_service = node.get("export_service", None)
        node_type = (node.get("type", "standard") or "standard").lower()
        if not export_service:
            return False
        if export_service not in ExportReplacements.SERVICES:
            raise CLIPipeException(f"Invalid export service: {export_service}")
        if node_type not in ExportReplacements.NODE_TYPES:
            raise CLIPipeException(f"Invalid export node type: {node_type}")
        return True

    @staticmethod
    def get_params_from_datafile(node: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
        """Returns the export parameters for a given node."""
        params = {}
        for datafile_key, export_key, default_value in ExportReplacements._REPLACEMENTS:
            if datafile_key == "export_schedule" and node.get(datafile_key, None) == "@on-demand":
                node[datafile_key] = ""
            params[export_key] = node[datafile_key] if datafile_key in node else default_value
        return params

    @staticmethod
    def get_datafile_key(param: str) -> Optional[str]:
        """Returns the datafile key for a given export parameter."""
        for datafile_k, export_k, _ in ExportReplacements._REPLACEMENTS:
            if export_k == param.lower():
                return datafile_k.upper()
        return None


requests_get = sync_to_async(requests.get, thread_sensitive=False)
requests_delete = sync_to_async(requests.delete, thread_sensitive=False)

pp = pprint.PrettyPrinter()


class AlreadyExistsException(click.ClickException):
    pass


class ParseException(Exception):
    def __init__(self, err: str, lineno: int = -1):
        self.lineno: int = lineno
        super().__init__(err)


class ValidationException(Exception):
    def __init__(self, err: str, lineno: int = -1) -> None:
        self.lineno: int = lineno
        super().__init__(err)


def sizeof_fmt(num: Union[int, float], suffix: str = "b") -> str:
    """Readable file size
    :param num: Bytes value
    :type num: int
    :param suffix: Unit suffix (optionnal) default = o
    :type suffix: str
    :rtype: str
    """
    for unit in ["", "k", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)


def is_shared_datasource(ds_name: str) -> bool:
    """just looking for a dot in the name is fine, dot are not allowed in regular datasources"""
    return "." in ds_name


class CLIGitRelease:
    NO_DATAFILES_PATHS = ["vendor/", "tests/", "scripts/"]
    DATAFILES_SUFFIXES = [".datasource", ".pipe", ".incl", ".token"]

    class ChangeType(Enum):
        # change type = T
        NEW_FILE = "A"
        COPIED = "C"
        MODIFIED = "M"
        RENAMED = "R"
        DELETED = "D"

        def as_feedback_message(self, diff: Diff) -> str:
            change_type = self.name.lower().replace("_", " ")
            changed = f"{diff.a_path} -> {diff.b_path}" if self.value == self.RENAMED.value else f"{diff.a_path}"  # type: ignore
            return FeedbackManager.info_git_release_diff(change_type=change_type, datafile_changed=changed)

    def __init__(self, path=None):
        try:
            self.repo = Repo(path, search_parent_directories=True)
            self.path = path or os.getcwd()
        except InvalidGitRepositoryError as exc:
            raise CLIGitReleaseException(FeedbackManager.error_no_git_repo_for_release(path=str(exc)))

    def working_dir(self):
        return self.repo.working_dir

    def status(self):
        return self.repo.git.status(self.path, "-s")

    def head(self) -> HEAD:
        return self.repo.head

    def head_commit(self) -> str:
        return self.head().commit.hexsha

    def is_head_empty(self) -> bool:
        return not self.repo.head.is_valid()

    def is_head_outdated(self, current_ws_commit: str) -> bool:
        try:
            return self.repo.is_ancestor(current_ws_commit, self.head_commit())
        except GitCommandError:
            raise CLIGitReleaseException(
                FeedbackManager.error_in_git_ancestor_commits(
                    head_commit=self.head().commit.hexsha, workspace_commit=current_ws_commit
                )
            )

    def has_untracked_files(self) -> bool:
        current_pwd = os.getcwd()
        working_dir = f"{self.repo.working_dir}/" if os.getcwd() != self.repo.working_dir else self.repo.working_dir
        project_path = current_pwd[current_pwd.startswith(working_dir) and len(working_dir) :]
        for untracked_file in self.repo.untracked_files:
            for path in PROJECT_PATHS:
                if untracked_file.startswith(f"{project_path}/{path}/" if project_path else f"{path}/"):
                    return True
        return False

    def is_dirty_to_release(self) -> bool:
        return self.repo.is_dirty(path=self.path) or self.has_untracked_files()

    def is_dirty_to_init(self) -> bool:
        return self.is_dirty_to_release() or self.is_head_empty()

    def is_new_release(self, current_ws_commit: str) -> bool:
        return self.head().commit.hexsha != current_ws_commit

    def diff(self, current_ws_commit: str) -> List[Diff]:
        return self.repo.commit(current_ws_commit).diff(self.head(), paths=self.path)

    def diff_datafiles(self, current_ws_commit: str) -> List[Diff]:
        # ignore diffs if:
        # not having a_path
        # not in data files paths
        # not expected suffixes
        return list(
            filter(
                lambda d: d.change_type in [c.value for c in self.ChangeType]
                and d.a_path
                and d.a_path not in self.NO_DATAFILES_PATHS
                and Path(d.a_path).resolve().suffix in self.DATAFILES_SUFFIXES,
                self.diff(current_ws_commit),
            )
        )

    def is_dottinyb_ignored(self) -> bool:
        return bool(self.repo.ignored(".tinyb"))

    def is_dotdifftemp_ignored(self) -> bool:
        return bool(self.repo.ignored(".diff_tmp")) or bool(self.repo.ignored(".diff_tmp/"))

    def validate_local_for_release(
        self,
        current_release: Dict[str, Any],
        check_dirty: bool = True,
        check_outdated: bool = True,
        check_new: bool = True,
    ):
        if self.is_dirty_to_release() and check_dirty:
            raise CLIGitReleaseException(
                FeedbackManager.error_commit_changes_to_release(path=self.path, git_output=self.status())
            )
        elif not self.is_head_outdated(current_release["commit"]) and check_outdated:
            raise CLIGitReleaseException(FeedbackManager.error_head_outdated(commit=self.head_commit()))
        elif not self.is_new_release(current_release["commit"]) and check_new:
            raise CLIGitReleaseException(FeedbackManager.error_head_already_released(commit=current_release["commit"]))

    def get_changes_from_diffs(self, diffs: List[Diff], filenames: List[str]):
        changed = {}
        parsed_resources: Dict[str, Datafile] = {}

        def _is_include(include_path, resource_path):
            if filename.endswith(".pipe"):
                parsed_func = parse_pipe
            else:
                parsed_func = parse_datasource
            parsed_resource = parsed_resources.get(resource_path, parsed_func(resource_path))
            parsed_resources[filename] = parsed_resource
            for include in parsed_resource.includes.keys():
                if Path(include_path).resolve().stem in include.strip('"').strip("'"):
                    return True
            return False

        for diff in diffs:
            # should be already filtered in diff_datafiles. make mypy happy
            if diff.a_path:
                if ".incl" in diff.a_path:
                    for filename in filenames:
                        if _is_include(diff.a_path, filename):
                            changed[Path(filename).resolve().stem] = diff.change_type
                else:
                    changed[Path(diff.a_path).resolve().stem] = diff.change_type

        # 'D' deleted are ignored
        return {
            Path(filename).resolve().stem: changed[Path(filename).resolve().stem]
            if Path(filename).resolve().stem in changed
            else None
            for filename in filenames
        }

    async def update_release(
        self, tb_client: TinyB, current_ws: Dict[str, Any], commit: Optional[str] = None
    ) -> Dict[str, Any]:
        release = await tb_client.workspace_commit_update(
            current_ws["id"], self.head().commit.hexsha if not commit else commit
        )
        return release


class Datafile:
    def __init__(self) -> None:
        self.maintainer: Optional[str] = None
        self.sources: List[str] = []
        self.nodes: List[Dict[str, Any]] = []
        self.tokens: List[Dict[str, Any]] = []
        self.keys: List[Dict[str, Any]] = []
        self.version: Optional[int] = None
        self.description: Optional[str] = None
        self.raw: Optional[List[str]] = None
        self.includes: Dict[str, Any] = {}
        self.shared_with: List[str] = []

    def validate(self) -> None:
        for x in self.nodes:
            if not x["name"].strip():
                raise ValidationException("invalid node name, can't be empty")
            if "sql" not in x:
                raise ValidationException("node %s must have a SQL query" % x["name"])
        if self.version is not None and (not isinstance(self.version, int) or self.version < 0):
            raise ValidationException("version must be a positive integer")

    def is_equal(self, other):
        if len(self.nodes) != len(other.nodes):
            return False

        for i, _ in enumerate(self.nodes):
            if self.nodes[i] != other.nodes[i]:
                return False

        return True


def parse_datasource(filename: str) -> Datafile:
    with open(filename) as file:
        s = file.read()
    basepath = os.path.dirname(filename)

    try:
        doc = parse(s, "default", basepath)
    except ParseException as e:
        raise click.ClickException(
            FeedbackManager.error_parsing_file(filename=filename, lineno=e.lineno, error=e)
        ) from None

    if len(doc.nodes) > 1:
        raise ValueError(f"{filename}: datasources can't have more than one node")

    return doc


def parse_pipe(filename: str) -> Datafile:
    with open(filename) as file:
        s = file.read()
    basepath = os.path.dirname(filename)

    try:
        sql = ""
        doc = parse(s, basepath=basepath)
        for node in doc.nodes:
            sql = node.get("sql", "")
            if sql.strip()[0] == "%":
                sql, _ = render_sql_template(sql[1:], test_mode=True, name=node["name"])
            # it'll fail with a ModuleNotFoundError when the toolset is not available but it returns the parsed doc
            from tinybird.sql_toolset import format_sql as toolset_format_sql

            toolset_format_sql(sql)
    except ParseException as e:
        raise click.ClickException(
            FeedbackManager.error_parsing_file(
                filename=filename, lineno=e.lineno, error=f"{str(e)} + SQL(parse exception): {sql}"
            )
        )
    except ValueError as e:
        raise click.ClickException(
            FeedbackManager.error_parsing_file(
                filename=filename, lineno="", error=f"{str(e)} + SQL(value error): {sql}"
            )
        )
    except UnClosedIfError as e:
        raise click.ClickException(
            FeedbackManager.error_parsing_node_with_unclosed_if(node=e.node, pipe=filename, lineno=e.lineno, sql=e.sql)
        )
    except ModuleNotFoundError:
        pass

    return doc


def parse_token(filename: str) -> Datafile:
    with open(filename) as file:
        s = file.read()
    basepath = os.path.dirname(filename)

    try:
        sql = ""
        doc = parse(s, basepath=basepath)
    except ParseException as e:
        raise click.ClickException(
            FeedbackManager.error_parsing_file(
                filename=filename, lineno=e.lineno, error=f"{str(e)} + SQL(parse exception): {sql}"
            )
        )
    except ValueError as e:
        raise click.ClickException(
            FeedbackManager.error_parsing_file(
                filename=filename, lineno="", error=f"{str(e)} + SQL(value error): {sql}"
            )
        )
    except UnClosedIfError as e:
        raise click.ClickException(
            FeedbackManager.error_parsing_node_with_unclosed_if(node=e.node, pipe=filename, lineno=e.lineno, sql=e.sql)
        )
    except ModuleNotFoundError:
        pass

    return doc


def _unquote(x: str):
    QUOTES = ('"', "'")
    if x[0] in QUOTES and x[-1] in QUOTES:
        x = x[1:-1]
    return x


def eval_var(s: str) -> str:
    # replace ENV variables
    # it's probably a bad idea to allow to get any env var
    return Template(s).safe_substitute(os.environ)


def parse(s: str, default_node: Optional[str] = None, basepath: str = ".") -> Datafile:  # noqa: C901
    """
    Parses `s` string into a document
    >>> d = parse("FROM SCRATCH\\nSOURCE 'https://example.com'\\n#this is a comment\\nMAINTAINER 'rambo' #this is me\\nNODE \\"test_01\\"\\n    DESCRIPTION this is a node that does whatever\\nSQL >\\n\\n        SELECT * from test_00\\n\\n\\nNODE \\"test_02\\"\\n    DESCRIPTION this is a node that does whatever\\nSQL >\\n\\n    SELECT * from test_01\\n    WHERE a > 1\\n    GROUP by a\\n")
    >>> d.maintainer
    'rambo'
    >>> d.sources
    ['https://example.com']
    >>> len(d.nodes)
    2
    >>> d.nodes[0]
    {'name': 'test_01', 'description': 'this is a node that does whatever', 'sql': 'SELECT * from test_00'}
    >>> d.nodes[1]
    {'name': 'test_02', 'description': 'this is a node that does whatever', 'sql': 'SELECT * from test_01\\nWHERE a > 1\\nGROUP by a'}
    """
    lines = list(StringIO(s, newline=None))

    doc = Datafile()
    doc.raw = list(StringIO(s, newline=None))

    parser_state = namedtuple("parser_state", ["multiline", "current_node", "command", "multiline_string", "is_sql"])

    parser_state.multiline = False
    parser_state.current_node = False

    def assign(attr):
        def _fn(x, **kwargs):
            setattr(doc, attr, _unquote(x))

        return _fn

    def schema(*args, **kwargs):
        s = _unquote("".join(args))
        try:
            sh = parse_table_structure(s)
        except Exception as e:
            raise ParseException(FeedbackManager.error_parsing_schema(line=kwargs["lineno"], error=e))
        parser_state.current_node["schema"] = ",".join(schema_to_sql_columns(sh))
        parser_state.current_node["columns"] = sh

    def assign_var(v: str) -> Callable[[VarArg(str), KwArg(Any)], None]:
        def _f(*args: str, **kwargs: Any):
            s = _unquote((" ".join(args)).strip())
            parser_state.current_node[v.lower()] = eval_var(s)

        return _f

    def sources(x: str, **kwargs: Any) -> None:
        doc.sources.append(_unquote(x))

    def node(*args: str, **kwargs: Any) -> None:
        node = {"name": eval_var(_unquote(args[0]))}
        doc.nodes.append(node)
        parser_state.current_node = node

    def scope(*args: str, **kwargs: Any) -> None:
        scope = {"name": eval_var(_unquote(args[0]))}
        doc.nodes.append(scope)
        parser_state.current_node = scope

    def description(*args: str, **kwargs: Any) -> None:
        description = (" ".join(args)).strip()

        if parser_state.current_node:
            parser_state.current_node["description"] = description
            if parser_state.current_node.get("name", "") == "default":
                doc.description = description
        else:
            doc.description = description

    def sql(var_name: str, **kwargs: Any) -> Callable[[str, KwArg(Any)], None]:
        def _f(sql: str, **kwargs: Any) -> None:
            if not parser_state.current_node:
                raise ParseException("SQL must be called after a NODE command")
            parser_state.current_node[var_name] = (
                textwrap.dedent(sql).rstrip() if "%" not in sql.strip()[0] else sql.strip()
            )

        # HACK this cast is needed because Mypy
        return cast(Callable[[str, KwArg(Any)], None], _f)

    def assign_node_var(v: str) -> Callable[[VarArg(str), KwArg(Any)], None]:
        def _f(*args: str, **kwargs: Any) -> None:
            if not parser_state.current_node:
                raise ParseException("%s must be called after a NODE command" % v)
            return assign_var(v)(*args, **kwargs)

        return _f

    def add_token(*args: str, **kwargs: Any) -> None:  # token_name, permissions):
        if len(args) < 2:
            raise ParseException('TOKEN gets two params, token name and permissions e.g TOKEN "read api token" READ')
        doc.tokens.append({"token_name": _unquote(args[0]), "permissions": args[1]})

    def add_key(*args: str, **kwargs: Any) -> None:  # token_name, permissions):
        if len(args) < 1:
            raise ParseException("KEY gets one params")
        doc.keys.append({"column": _unquote(args[0])})

    def test(*args: str, **kwargs: Any) -> None:
        print("test", args, kwargs)

    def include(*args: str, **kwargs: Any) -> None:
        f = _unquote(args[0])
        f = eval_var(f)
        attrs = dict(_unquote(x).split("=", 1) for x in args[1:])
        nonlocal lines
        lineno = kwargs["lineno"]
        n = lineno
        args_with_attrs = " ".join(args)
        try:
            while True:
                n += 1
                if len(lines) <= n:
                    break
                if "NODE" in lines[n]:
                    doc.includes[args_with_attrs] = lines[n]
                    break
            if args_with_attrs not in doc.includes:
                doc.includes[args_with_attrs] = ""
        except Exception:
            pass
        # be sure to replace the include line
        p = Path(basepath)
        with open(p / f) as file:
            try:
                ll = list(StringIO(file.read(), newline=None))
                node_line = [line for line in ll if "NODE" in line]
                if node_line and doc.includes[args_with_attrs]:
                    doc.includes[node_line[0].split("NODE")[-1].split("\n")[0].strip()] = ""
            except Exception:
                pass
            finally:
                file.seek(0)
            lines[lineno : lineno + 1] = [""] + list(
                StringIO(Template(file.read()).safe_substitute(attrs), newline=None)
            )

    def version(*args: str, **kwargs: Any) -> None:
        if len(args) < 1:
            raise ParseException("VERSION gets one positive integer param")
        try:
            version = int(args[0])
            if version < 0:
                raise ValidationException("version must be a positive integer e.g VERSION 2")
            doc.version = version
        except ValueError:
            raise ValidationException("version must be a positive integer e.g VERSION 2")

    def shared_with(*args: str, **kwargs: Any) -> None:
        for entries in args:
            # In case they specify multiple workspaces
            doc.shared_with += [workspace.strip() for workspace in entries.splitlines()]

    def __init_engine(v: str):
        if not parser_state.current_node:
            raise Exception(f"{v} must be called after a NODE command")
        if "engine" not in parser_state.current_node:
            parser_state.current_node["engine"] = {"type": None, "args": []}

    def set_engine(*args: str, **kwargs: Any) -> None:
        __init_engine("ENGINE")
        engine_type = _unquote((" ".join(args)).strip())
        parser_state.current_node["engine"]["type"] = engine_type

    def add_engine_var(v: str) -> Callable[[VarArg(str), KwArg(Any)], None]:
        def _f(*args: str, **kwargs: Any):
            __init_engine(f"ENGINE_{v}".upper())
            engine_arg = _unquote((" ".join(args)).strip())
            parser_state.current_node["engine"]["args"].append((v, engine_arg))

        return _f

    cmds = {
        "from": assign("from"),
        "source": sources,
        "maintainer": assign("maintainer"),
        "schema": schema,
        "engine": set_engine,
        "partition_key": assign_var("partition_key"),
        "sorting_key": assign_var("sorting_key"),
        "primary_key": assign_var("primary_key"),
        "sampling_key": assign_var("sampling_key"),
        "ttl": assign_var("ttl"),
        "settings": assign_var("settings"),
        "node": node,
        "scope": scope,
        "description": description,
        "type": assign_node_var("type"),
        "datasource": assign_node_var("datasource"),
        "tags": assign_node_var("tags"),
        "target_datasource": assign_node_var("target_datasource"),
        "copy_schedule": assign_node_var("copy_schedule"),
        "resource": assign_node_var("resource"),
        "filter": assign_node_var("filter"),
        "token": add_token,
        "key": add_key,
        "test": test,
        "include": include,
        "sql": sql("sql"),
        "version": version,
        "kafka_connection_name": assign_var("kafka_connection_name"),
        "kafka_topic": assign_var("kafka_topic"),
        "kafka_group_id": assign_var("kafka_group_id"),
        "kafka_bootstrap_servers": assign_var("kafka_bootstrap_servers"),
        "kafka_key": assign_var("kafka_key"),
        "kafka_secret": assign_var("kafka_secret"),
        "kafka_schema_registry_url": assign_var("kafka_schema_registry_url"),
        "kafka_target_partitions": assign_var("kafka_target_partitions"),
        "kafka_auto_offset_reset": assign_var("kafka_auto_offset_reset"),
        "kafka_store_raw_value": assign_var("kafka_store_raw_value"),
        "kafka_store_headers": assign_var("kafka_store_headers"),
        "kafka_key_avro_deserialization": assign_var("kafka_key_avro_deserialization"),
        "import_service": assign_var("import_service"),
        "import_connection_name": assign_var("import_connection_name"),
        "import_schedule": assign_var("import_schedule"),
        "import_strategy": assign_var("import_strategy"),
        "import_external_datasource": assign_var("import_external_datasource"),
        "import_bucket_uri": assign_var("import_bucket_uri"),
        "import_query": assign_var("import_query"),
        "shared_with": shared_with,
        "export_service": assign_var("export_service"),
        "export_connection_name": assign_var("export_connection_name"),
        "export_schedule": assign_var("export_schedule"),
        "export_bucket_uri": assign_var("export_bucket_uri"),
        "export_file_template": assign_var("export_file_template"),
        "export_format": assign_var("export_format"),
        "export_strategy": assign_var("export_strategy"),
        "export_compression": assign_var("export_compression"),
    }

    engine_vars = set()

    for _engine, (params, options) in ENABLED_ENGINES:
        for p in params:
            engine_vars.add(p.name)
        for o in options:
            engine_vars.add(o.name)
    for v in engine_vars:
        cmds[f"engine_{v}"] = add_engine_var(v)

    if default_node:
        node(default_node)

    lineno = 0
    try:
        while lineno < len(lines):
            line = lines[lineno]
            try:
                sa = shlex.shlex(line)
                sa.whitespace_split = True
                lexer = list(sa)
            except ValueError:
                sa = shlex.shlex(shlex.quote(line))
                sa.whitespace_split = True
                lexer = list(sa)
            if lexer:
                cmd, args = lexer[0], lexer[1:]

                if (
                    parser_state.multiline
                    and cmd.lower() in cmds
                    and not (line.startswith(" ") or line.startswith("\t") or line.lower().startswith("from"))
                ):
                    parser_state.multiline = False
                    cmds[parser_state.command](parser_state.multiline_string, lineno=lineno)

                if not parser_state.multiline:
                    if len(args) >= 1 and args[0] == ">":
                        parser_state.multiline = True
                        parser_state.command = cmd.lower()
                        parser_state.multiline_string = ""
                    else:
                        if cmd.lower() in cmds:
                            cmds[cmd.lower()](*args, lineno=lineno)
                        else:
                            raise click.ClickException(FeedbackManager.error_option(option=cmd.upper()))
                else:
                    parser_state.multiline_string += line
            lineno += 1
        # close final state
        if parser_state.multiline:
            cmds[parser_state.command](parser_state.multiline_string, lineno=lineno)
    except ParseException as e:
        raise ParseException(str(e), lineno=lineno)
    except ValidationException as e:
        raise ValidationException(str(e), lineno=lineno)
    except IndexError as e:
        if "node" in line.lower():
            raise click.ClickException(FeedbackManager.error_missing_node_name())
        elif "sql" in line.lower():
            raise click.ClickException(FeedbackManager.error_missing_sql_command())
        elif "datasource" in line.lower():
            raise click.ClickException(FeedbackManager.error_missing_datasource_name())
        else:
            raise ValidationException(f"Validation error, found {line} in line {str(lineno)}: {str(e)}", lineno=lineno)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        raise ParseException(f"Unexpected error: {e}", lineno=lineno)

    return doc


def generate_resource_for_key(key: str, name: str, schema: str, version: str, res_name: str) -> List[Dict[str, Any]]:
    resources: List[Dict[str, Any]] = []
    # datasource
    ds_name = f"{name}_join_by_{key}{version}"
    params = {
        "name": ds_name,
        "schema": schema,
        "engine": "Join",
        "engine_join_strictness": "ANY",
        "engine_join_type": "LEFT",
        "engine_key_columns": key,
    }
    resources.append(
        {
            "resource_name": f"{name}_join_by_{key}",
            "resource": "datasources",
            "params": params,
            "filename": f"{params['name']}.datasource",
        }
    )
    resources.append(
        {
            "resource_name": f"{name}_join_by_{key}_pipe",
            "resource": "pipes",
            "filename": f"{params['name']}.pipe",
            "name": f"{name}_join_by_{key}_pipe{version}",
            "schema": schema,
            "nodes": [
                {
                    "sql": f"select * from {name}{version}",
                    "params": {"name": f"{name}_join_by_{key}_view", "type": "materialized", "datasource": ds_name},
                }
            ],
            "deps": [res_name],  # [ds_name],
            "tokens": [],
        }
    )
    return resources


async def process_file(
    filename: str,
    tb_client: TinyB,
    tag: Optional[str] = "",
    resource_versions: Optional[Dict] = None,
    skip_connectors: bool = False,
    workspace_map: Optional[Dict] = None,
    workspace_lib_paths: Optional[List[Tuple[str, str]]] = None,
    current_ws: Optional[Dict[str, Any]] = None,
):  # noqa: C901 B006
    if workspace_map is None:
        workspace_map = {}

    if resource_versions is None:
        resource_versions = {}
    resource_versions_string = {k: f"__v{v}" for k, v in resource_versions.items() if v >= 0}

    def get_engine_params(node: Dict[str, Any]) -> Dict[str, Any]:
        params = {}

        if "engine" in node:
            engine = node["engine"]["type"]
            params["engine"] = engine
            args = node["engine"]["args"]
            for k, v in args:
                params[f"engine_{k}"] = v
        return params

    async def get_kafka_params(node: Dict[str, Any]):
        params = {key: value for key, value in node.items() if key.startswith("kafka")}

        if not skip_connectors:
            try:
                connector_params = {
                    "kafka_bootstrap_servers": params.get("kafka_bootstrap_servers", None),
                    "kafka_key": params.get("kafka_key", None),
                    "kafka_secret": params.get("kafka_secret", None),
                    "kafka_connection_name": params.get("kafka_connection_name", None),
                    "kafka_auto_offset_reset": params.get("kafka_auto_offset_reset", None),
                    "kafka_schema_registry_url": params.get("kafka_schema_registry_url", None),
                }

                connector = await tb_client.get_connection(**connector_params)

                if not connector:
                    click.echo(
                        FeedbackManager.info_creating_kafka_connection(connection_name=params["kafka_connection_name"])
                    )
                    required_params = [
                        connector_params["kafka_bootstrap_servers"],
                        connector_params["kafka_key"],
                        connector_params["kafka_secret"],
                    ]

                    if not all(required_params):
                        raise Exception(FeedbackManager.error_unknown_kafka_connection(datasource=name))

                    connector = await tb_client.connection_create_kafka(**connector_params)
            except Exception as e:
                raise click.ClickException(
                    FeedbackManager.error_connection_create(
                        connection_name=params["kafka_connection_name"], error=str(e)
                    )
                )

            click.echo(FeedbackManager.success_connection_using(connection_name=connector["name"]))

            params.update(
                {
                    "connector": connector["id"],
                    "service": "kafka",
                }
            )

        return params

    async def get_import_params(datasource: Dict[str, Any], node: Dict[str, Any]) -> Dict[str, Any]:
        params: Dict[str, Any] = {key: value for key, value in node.items() if key.startswith("import_")}

        if len(params) == 0 or skip_connectors:
            return params

        service: Optional[str] = node.get("import_service", None)

        if service and service.lower() == "bigquery":
            if not await tb_client.check_gcp_read_permissions():
                raise Exception(FeedbackManager.error_unknown_bq_connection(datasource=datasource["name"]))

            # Bigquery doesn't have a datalink, so we can stop here
            return params

        # Rest of connectors

        connector_id: Optional[str] = node.get("import_connector", None)
        connector_name: Optional[str] = node.get("import_connection_name", None)
        if not connector_name and not connector_id:
            raise Exception(FeedbackManager.error_missing_connection_name(datasource=datasource["name"]))

        if not connector_id:
            assert isinstance(connector_name, str)

            connector: Optional[Dict[str, Any]] = await tb_client.get_connector(connector_name, service)

            if not connector:
                raise Exception(
                    FeedbackManager.error_unknown_connection(datasource=datasource["name"], connection=connector_name)
                )
            connector_id = connector["id"]
            service = connector["service"]

        # The API needs the connector ID to create the datasource.
        params["import_connector"] = connector_id
        if service:
            params["import_service"] = service

        if service == "s3":
            if not params.get("import_bucket_uri", None):
                raise Exception(FeedbackManager.error_missing_bucket_uri(datasource=datasource["name"]))
        else:
            if not params.get("import_external_datasource", None):
                raise Exception(FeedbackManager.error_missing_external_datasource(datasource=datasource["name"]))

        return params

    if DataFileExtensions.DATASOURCE in filename:
        doc = parse_datasource(filename)
        node = doc.nodes[0]
        deps: List[str] = []
        # reemplace tables on materialized columns
        columns = parse_table_structure(node["schema"])

        _format = "csv"
        for x in columns:
            if x["default_value"] and x["default_value"].lower().startswith("materialized"):
                # turn expression to a select query to sql_get_used_tables can get the used tables
                q = "select " + x["default_value"][len("materialized") :]
                tables = await tb_client.sql_get_used_tables(q)
                # materialized columns expressions could have joins so we need to add them as a dep
                deps += tables
                # generate replacements and replace the query
                replacements = {t: t + resource_versions_string.get(t, "") for t in tables}

                replaced_results = await tb_client.replace_tables(q, replacements)
                x["default_value"] = replaced_results.replace("SELECT", "materialized", 1)
            if x.get("jsonpath", None):
                _format = "ndjson"

        schema = ",".join(schema_to_sql_columns(columns))

        name = os.path.basename(filename).rsplit(".", 1)[0]

        if workspace_lib_paths:
            for wk_name, wk_path in workspace_lib_paths:
                try:
                    Path(filename).relative_to(wk_path)
                    name = f"{workspace_map.get(wk_name, wk_name)}.{name}"
                except ValueError:
                    # the path was not relative, not inside workspace
                    pass
        #
        res_name = name
        if tag and not is_shared_datasource(name):
            name = f"{tag}__{name}"

        version = f"__v{doc.version}" if doc.version is not None else ""

        def append_version_to_name(name: str, version: str) -> str:
            if version != "":
                name = name.replace(".", "_")
                return name + version
            return name

        description = node.get("description", "")
        params = {
            "name": append_version_to_name(name, version),
            "description": description,
            "schema": schema,
            "format": _format,
        }

        params.update(get_engine_params(node))

        if "import_service" in node or "import_connection_name" in node:
            VALID_SERVICES: Tuple[str, ...] = ("bigquery", "snowflake", "s3")

            import_params = await get_import_params(params, node)

            service = import_params.get("import_service", None)
            if service and service not in VALID_SERVICES:
                raise Exception(f"Unknown import service: {service}")

            if service == "s3":
                ON_DEMAND_CRON = "@on-demand"
                AUTO_CRON = "@auto"
                ON_DEMAND_CRON_EXPECTED_BY_THE_API = "@once"
                VALID_CRONS: Tuple[str, ...] = (ON_DEMAND_CRON, AUTO_CRON)
                cron = node.get("import_schedule", ON_DEMAND_CRON)

                if cron not in VALID_CRONS:
                    valid_values = ", ".join(VALID_CRONS)
                    raise Exception(f"Invalid import schedule: '{cron}'. Valid values are: {valid_values}")

                if cron == ON_DEMAND_CRON:
                    import_params["import_schedule"] = ON_DEMAND_CRON_EXPECTED_BY_THE_API
                if cron == AUTO_CRON and current_ws:
                    workspaces = (await tb_client.user_workspaces()).get("workspaces", [])
                    rate_limits: Dict[str, Dict[str, int]] = next(
                        (w.get("rate_limits", {}) for w in workspaces if w["id"] == current_ws["id"]), {}
                    )
                    period: int = rate_limits.get("api_datasources_create_append_replace", {}).get("period", 60)

                    def seconds_to_cron_expression(seconds: int) -> str:
                        minutes = seconds // 60
                        hours = minutes // 60
                        days = hours // 24
                        if days > 0:
                            return f"0 0 */{days} * *"
                        if hours > 0:
                            return f"0 */{hours} * * *"
                        if minutes > 0:
                            return f"*/{minutes} * * * *"
                        return f"*/{seconds} * * * *"

                    import_params["import_schedule"] = seconds_to_cron_expression(period)

            # Include all import_ parameters in the datasource params
            params.update(import_params)

            # Substitute the import parameters with the ones used by the
            # import API:
            # - If an import parameter is not present and there's a default
            #   value, use the default value.
            # - If the resulting value is None, do not add the parameter.
            #
            # Note: any unknown import_ parameter is leaved as is.
            for key in ImportReplacements.get_datafile_parameter_keys():
                replacement, default_value = ImportReplacements.get_api_param_for_datafile_param(service, key)
                if not replacement:
                    continue  # We should not reach this never, but just in case...

                value: Any
                try:
                    value = params[key]
                    del params[key]
                except KeyError:
                    value = default_value

                if value:
                    params[replacement] = value

        if "kafka_connection_name" in node:
            kafka_params = await get_kafka_params(node)
            params.update(kafka_params)
            del params["format"]

        if "tags" in node:
            tags = {k: v[0] for k, v in urllib.parse.parse_qs(node["tags"]).items()}
            params.update(tags)

        resources: List[Dict[str, Any]] = []

        resources.append(
            {
                "resource": "datasources",
                "resource_name": name,
                "version": doc.version,
                "params": params,
                "filename": filename,
                "keys": doc.keys,
                "deps": deps,
                "tokens": doc.tokens,
                "shared_with": doc.shared_with,
            }
        )

        # generate extra resources in case of the key
        if doc.keys:
            for k in doc.keys:
                resources += generate_resource_for_key(k["column"], name, params["schema"], version, res_name)
                # set derived resources version the same the parent
                for x in resources:
                    x["version"] = doc.version

        return resources

    elif DataFileExtensions.PIPE in filename:
        doc = parse_pipe(filename)
        version = f"__v{doc.version}" if doc.version is not None else ""
        name = os.path.basename(filename).split(".")[0]
        description = doc.description if doc.description is not None else ""

        if tag and not is_shared_datasource(name):
            name = f"{tag}__{name}"

        deps = []
        nodes: List[Dict[str, Any]] = []

        for node in doc.nodes:
            sql = node["sql"]
            node_type = node.get("type", "standard").lower()
            params = {
                "name": node["name"],
                "type": node_type,
                "description": node.get("description", ""),
                "target_datasource": node.get("target_datasource", None),
                "copy_schedule": node.get("copy_schedule", None),
            }

            is_export_node = ExportReplacements.is_export_node(node)
            export_params = ExportReplacements.get_params_from_datafile(node) if is_export_node else None

            sql = sql.strip()
            is_template = False
            if sql[0] == "%":
                try:
                    sql_rendered, _ = render_sql_template(sql[1:], test_mode=True)
                except Exception as e:
                    raise click.ClickException(
                        FeedbackManager.error_parsing_node(node=node["name"], pipe=name, error=str(e))
                    )
                is_template = True
            else:
                sql_rendered = sql

            try:
                dependencies = await tb_client.sql_get_used_tables(sql_rendered, raising=True)
                deps += [t for t in dependencies if t not in [n["name"] for n in doc.nodes]]

            except Exception as e:
                raise click.ClickException(
                    FeedbackManager.error_parsing_node(node=node["name"], pipe=name, error=str(e))
                )

            if is_template:
                deps += get_used_tables_in_template(sql[1:])

            tag_ = ""
            if tag:
                tag_ = f"{tag}__"

            is_neither_copy_nor_materialized = "datasource" not in node and "target_datasource" not in node
            if "engine" in node and is_neither_copy_nor_materialized:
                raise ValueError("Defining ENGINE options in a node requires a DATASOURCE")

            if "datasource" in node:
                params["datasource"] = (
                    tag_ + node["datasource"] + resource_versions_string.get(tag_ + node["datasource"], "")
                )
                deps += [node["datasource"]]

            if "target_datasource" in node:
                params["target_datasource"] = (
                    tag_
                    + node["target_datasource"]
                    + resource_versions_string.get(tag_ + node["target_datasource"], "")
                )
                deps += [node["target_datasource"]]

            params.update(get_engine_params(node))

            def create_replacement_for_resource(tag: str, name: str) -> str:
                for old_ws, new_ws in workspace_map.items():
                    name = name.replace(f"{old_ws}.", f"{new_ws}.")
                if tag != "" and not is_shared_datasource(name):
                    name = tag + name
                return name + resource_versions_string.get(name, "")

            replacements = {
                x: create_replacement_for_resource(tag_, x) for x in deps if x not in [n["name"] for n in doc.nodes]
            }

            # FIXME: Ideally we should use await tb_client.replace_tables(sql, replacements)
            for old, new in replacements.items():
                sql = re.sub("([\t \\n']+|^)" + old + "([\t \\n'\\)]+|$)", "\\1" + new + "\\2", sql)

            if "tags" in node:
                tags = {k: v[0] for k, v in urllib.parse.parse_qs(node["tags"]).items()}
                params.update(tags)

            nodes.append(
                {
                    "sql": sql,
                    "params": params,
                    "export_params": export_params,
                }
            )

        return [
            {
                "resource": "pipes",
                "resource_name": name,
                "version": doc.version,
                "filename": filename,
                "name": name + version,
                "nodes": nodes,
                "deps": [x for x in set(deps)],
                "tokens": doc.tokens,
                "description": description,
            }
        ]
    elif DataFileExtensions.TOKEN in filename:
        doc = parse_token(filename)
        name = os.path.basename(filename).split(DataFileExtensions.TOKEN)[0]
        description = doc.description or ""
        version = f"__v{doc.version}" if doc.version is not None else ""
        scopes = doc.nodes or []
        return [
            {
                "resource": "tokens",
                "resource_name": name,
                "version": doc.version,
                "filename": filename,
                "name": name + version,
                "scopes": scopes,
                "description": description,
            }
        ]
    else:
        raise Exception(FeedbackManager.error_file_extension(filename=filename))


def full_path_by_name(
    folder: str, name: str, workspace_lib_paths: Optional[List[Tuple[str, str]]] = None
) -> Optional[Path]:
    f = Path(folder)
    ds = name + ".datasource"
    if os.path.isfile(os.path.join(folder, ds)):
        return f / ds
    if os.path.isfile(f / "datasources" / ds):
        return f / "datasources" / ds

    pipe = name + ".pipe"
    if os.path.isfile(os.path.join(folder, pipe)):
        return f / pipe

    if os.path.isfile(f / "endpoints" / pipe):
        return f / "endpoints" / pipe

    if os.path.isfile(f / "pipes" / pipe):
        return f / "pipes" / pipe

    token = name + ".token"
    if os.path.isfile(f / "tokens" / token):
        return f / "tokens" / token

    if workspace_lib_paths:
        for wk_name, wk_path in workspace_lib_paths:
            if name.startswith(f"{wk_name}."):
                r = full_path_by_name(wk_path, name.replace(f"{wk_name}.", ""))
                if r:
                    return r
    return None


def find_file_by_name(
    folder: str,
    name: str,
    verbose: bool = False,
    is_raw: bool = False,
    workspace_lib_paths: Optional[List[Tuple[str, str]]] = None,
    resource: Optional[Dict] = None,
    deps_tag: str = "",
):
    f = Path(folder)
    ds = name + ".datasource"
    if os.path.isfile(os.path.join(folder, ds)):
        return ds, None
    if os.path.isfile(f / "datasources" / ds):
        return ds, None

    pipe = name + ".pipe"
    if os.path.isfile(os.path.join(folder, pipe)):
        return pipe, None

    if os.path.isfile(f / "endpoints" / pipe):
        return pipe, None

    if os.path.isfile(f / "pipes" / pipe):
        return pipe, None

    token = name + ".token"
    if os.path.isfile(f / "tokens" / token):
        return token, None

    # look for the file in subdirectories if it's not found in datasources folder
    if workspace_lib_paths:
        _resource = None
        for wk_name, wk_path in workspace_lib_paths:
            file = None
            if name.startswith(f"{wk_name}."):
                file, _resource = find_file_by_name(
                    wk_path, name.replace(f"{wk_name}.", ""), verbose, is_raw, resource=resource, deps_tag=deps_tag
                )
            if file:
                return file, _resource

    if not is_raw:
        f, raw = find_file_by_name(
            folder,
            get_dep_from_raw_tables(name),
            verbose=verbose,
            is_raw=True,
            workspace_lib_paths=workspace_lib_paths,
            resource=resource,
            deps_tag=deps_tag,
        )
        return f, raw

    # materialized node with DATASOURCE definition
    if resource and "nodes" in resource:
        for node in resource["nodes"]:
            params = node.get("params", {})
            if (
                params.get("type", None) == "materialized"
                and params.get("engine", None)
                and params.get("datasource", None)
            ):
                pipe = resource["resource_name"].replace(deps_tag, "") + ".pipe"
                pipe_file_exists = (
                    os.path.isfile(os.path.join(folder, pipe))
                    or os.path.isfile(f / "endpoints" / pipe)
                    or os.path.isfile(f / "pipes" / pipe)
                )
                is_target_datasource = params["datasource"] == name
                if pipe_file_exists and is_target_datasource:
                    return pipe, {"resource_name": params.get("datasource")}

    if verbose:
        click.echo(FeedbackManager.warning_file_not_found_inside(name=name, folder=folder))

    return None, None


def drop_token(url: str) -> str:
    """
    drops token param from the url query string
    >>> drop_token('https://api.tinybird.co/v0/pipes/aaa.json?token=abcd&a=1')
    'https://api.tinybird.co/v0/pipes/aaa.json?a=1'
    >>> drop_token('https://api.tinybird.co/v0/pipes/aaa.json?a=1')
    'https://api.tinybird.co/v0/pipes/aaa.json?a=1'
    """
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    qs_simplify = {k: v[0] for k, v in qs.items()}  # change several arguments to single one
    if "token" in qs_simplify:
        del qs_simplify["token"]
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urlencode(qs_simplify)}"


def normalize_array(items: List[Dict[str, Optional[Any]]]) -> List[Dict]:
    """
        Sorted() doesn't not support values with different types for the same column like None vs str.
        So, we need to cast all None to default value of the type of the column if exist and if all the values are None, we can leave them as None
    >>> normalize_array([{'x': 'hello World'}, {'x': None}])
    [{'x': 'hello World'}, {'x': ''}]
    >>> normalize_array([{'x': 3}, {'x': None}])
    [{'x': 3}, {'x': 0}]
    >>> normalize_array([{'x': {'y': [1,2,3,4]}}, {'x': {'z': "Hello" }}])
    [{'x': {'y': [1, 2, 3, 4]}}, {'x': {'z': 'Hello'}}]
    """
    types: Dict[str, type] = {}
    if len(items) == 0:
        return items

    columns = items[0].keys()
    for column in columns:
        for object in items:
            if object[column] is not None:
                types[column] = type(object[column])
                break

    for object in items:
        for column in columns:
            if object[column] is not None:
                continue

            # If None, we replace it for the default value
            if types.get(column, None):
                object[column] = types[column]()

    return items


class PipeChecker(unittest.TestCase):
    RETRIES_LIMIT = PIPE_CHECKER_RETRIES

    current_response_time: float = 0
    checker_response_time: float = 0

    current_read_bytes: int = 0
    checker_read_bytes: int = 0

    def __init__(
        self,
        current_pipe_url: str,
        pipe_name: str,
        checker_pipe_name: str,
        token: str,
        only_response_times: bool,
        ignore_order: bool,
        validate_processed_bytes: bool,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.current_pipe_url = (
            current_pipe_url.replace(".ndjson", ".json").replace(".csv", ".json").replace(".parquet", ".json")
        )
        self.current_pipe_url = drop_token(self.current_pipe_url)
        self.current_pipe_url += ("&" if "?" in self.current_pipe_url else "?") + "pipe_checker=true"
        self.checker_pipe_name = checker_pipe_name
        self.pipe_name = pipe_name
        self.token = token
        self.only_response_times = only_response_times
        self.ignore_order = ignore_order
        self.validate_processed_bytes = validate_processed_bytes
        parsed = urlparse(self.current_pipe_url)
        self.qs: Dict[Any, Any] = parse_qs(parsed.query)
        self.checker_pipe_url = (
            f"{parsed.scheme}://{parsed.netloc}/v0/pipes/{self.checker_pipe_name}.json?{parsed.query}"
        )

    def __str__(self):
        return f"current {self.current_pipe_url}\n    new {self.checker_pipe_url}"

    def diff(self, a: Dict[str, Any], b: Dict[str, Any]) -> str:
        a_properties = list(map(lambda x: f"{x}:{a[x]}\n", a.keys()))
        b_properties = list(map(lambda x: f"{x}:{b[x]}\n", b.keys()))

        return "".join(difflib.context_diff(a_properties, b_properties, self.pipe_name, self.checker_pipe_name))

    def _get_request_for_current(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        return requests.get(self.current_pipe_url, headers=headers)

    def _get_request_for_checker(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        return requests.get(self.checker_pipe_url, headers=headers)

    def _write_performance(self):
        return ""

    def _runTest(self) -> None:
        current_r = self._get_request_for_current()
        checker_r = self._get_request_for_checker()

        try:
            self.current_response_time = current_r.elapsed.total_seconds()
            self.checker_response_time = checker_r.elapsed.total_seconds()
        except Exception:
            pass

        current_response: Dict[str, Any] = current_r.json()
        checker_response: Dict[str, Any] = checker_r.json()

        current_data: List[Dict[str, Any]] = current_response.get("data", [])
        checker_data: List[Dict[str, Any]] = checker_response.get("data", [])

        self.current_read_bytes = current_response.get("statistics", {}).get("bytes_read", 0)
        self.checker_read_bytes = checker_response.get("statistics", {}).get("bytes_read", 0)

        error_check_fixtures_data: Optional[str] = checker_response.get("error", None)
        self.assertIsNone(
            error_check_fixtures_data,
            "You are trying to push a pipe with errors, please check the output or run with --no-check",
        )

        increase_response_time = (
            checker_r.elapsed.total_seconds() - current_r.elapsed.total_seconds()
        ) / current_r.elapsed.total_seconds()
        if self.only_response_times:
            self.assertLess(
                increase_response_time, 0.25, msg=f"response time has increased {round(increase_response_time * 100)}%"
            )
            return

        self.assertEqual(len(current_data), len(checker_data), "Number of elements does not match")

        if self.validate_processed_bytes:
            increase_read_bytes = (self.checker_read_bytes - self.current_read_bytes) / self.current_read_bytes
            self.assertLess(
                round(increase_read_bytes, 2),
                0.25,
                msg=f"The number of processed bytes has increased {round(increase_read_bytes * 100)}%",
            )

        if self.ignore_order:
            current_data = (
                sorted(normalize_array(current_data), key=itemgetter(*[k for k in current_data[0].keys()]))
                if len(current_data) > 0
                else current_data
            )
            checker_data = (
                sorted(normalize_array(checker_data), key=itemgetter(*[k for k in checker_data[0].keys()]))
                if len(checker_data) > 0
                else checker_data
            )

        for _, (current_data_e, check_fixtures_data_e) in enumerate(zip(current_data, checker_data)):
            self.assertEqual(list(current_data_e.keys()), list(check_fixtures_data_e.keys()))
            for x in current_data_e.keys():
                if type(current_data_e[x]) == float:
                    d = abs(current_data_e[x] - check_fixtures_data_e[x])
                    self.assertLessEqual(
                        d / current_data_e[x],
                        0.01,
                        f"key {x}. old value: {current_data_e[x]}, new value {check_fixtures_data_e[x]}\n{self.diff(current_data_e, check_fixtures_data_e)}",
                    )
                elif (
                    not isinstance(current_data_e[x], (str, bytes))
                    and isinstance(current_data_e[x], Iterable)
                    and self.ignore_order
                ):

                    def flatten(items):
                        """Yield items from any nested iterable; see Reference."""
                        output = []
                        for x in items:
                            if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
                                output.extend(flatten(x))
                            else:
                                output.append(x)
                        return output

                    self.assertEqual(
                        flatten(current_data_e[x]).sort(),
                        flatten(check_fixtures_data_e[x]).sort(),
                        "\n" + self.diff(current_data_e, check_fixtures_data_e),
                    )
                else:
                    self.assertEqual(
                        current_data_e[x],
                        check_fixtures_data_e[x],
                        "\n" + self.diff(current_data_e, check_fixtures_data_e),
                    )

    def runTest(self) -> None:
        if "debug" in self.qs or ("from" in self.qs and self.qs["from"] == "ui"):
            self.skipTest("found debug param")

        # Let's retry the validation to avoid false alerts when dealing with endpoints that have continuos ingestion
        retries = 0
        while retries < self.RETRIES_LIMIT:
            try:
                self._runTest()
            except AssertionError as e:
                retries += 1
                if retries >= self.RETRIES_LIMIT:
                    raise e
            else:
                break


@dataclass
class PipeCheckerRunnerResponse:
    pipe_name: str
    test_type: str
    output: str
    metrics_summary: Optional[Dict[str, Any]]
    metrics_timing: Dict[str, Tuple[float, float, float]]
    failed: List[Dict[str, str]]
    was_successfull: bool


class PipeCheckerRunner:
    checker_stream_result_class = unittest.runner._WritelnDecorator  # type: ignore

    def __init__(self, pipe_name: str, host: str):
        self.pipe_name = pipe_name
        self.host = host

    def get_sqls_for_requests_to_check(
        self,
        matches: List[str],
        sample_by_params: int,
        limit: int,
        pipe_stats_rt_table: str = "",
        extra_where_clause: str = "",
    ):
        pipe_stats_rt = pipe_stats_rt_table or "tinybird.pipe_stats_rt"
        sql_for_coverage = f"""
                        SELECT extractURLParameterNames(assumeNotNull(url)) as params, groupArraySample({sample_by_params if sample_by_params > 0 else 1})(url) as endpoint_url
                        FROM {pipe_stats_rt}
                        WHERE
                            url like '%/{self.pipe_name}.%'
                            AND url IS NOT NULL
                            AND extractURLParameter(assumeNotNull(url), 'from') <> 'ui'
                            AND extractURLParameter(assumeNotNull(url), 'pipe_checker') <> 'true'
                            AND extractURLParameter(assumeNotNull(url), 'debug') <> 'query'
                            AND error = 0
                            AND not has(params, '__tb__semver')
                            {" AND " + " AND ".join([f"has(params, '{match}')" for match in matches]) if matches and len(matches) > 0 else ''}
                            { extra_where_clause }
                        GROUP BY params
                        FORMAT JSON
                    """
        sql_latest_requests = f"""
                                SELECT groupArray(*) as endpoint_url
                                FROM (
                                    WITH extractURLParameterNames(assumeNotNull(url)) as params
                                    SELECT distinct(url)
                                    FROM {pipe_stats_rt}
                                    WHERE
                                        url like '%/{self.pipe_name}.%'
                                        AND url is not null
                                        AND extractURLParameter(assumeNotNull(url), 'from') <> 'ui'
                                        AND extractURLParameter(assumeNotNull(url), 'pipe_checker') <> 'true'
                                        AND extractURLParameter(assumeNotNull(url), 'debug') <> 'query'
                                        AND error = 0
                                        AND not has(params, '__tb__semver')
                                        {" AND " + " AND ".join([f"has(params, '{match}')" for match in matches]) if matches and len(matches) > 0 else ''}
                                        {extra_where_clause}
                                    LIMIT {limit}
                                )
                                FORMAT JSON
                            """
        return sql_for_coverage, sql_latest_requests

    def _get_checker(
        self,
        request: Dict[str, str],
        checker_pipe_name: str,
        token: str,
        only_response_times: bool,
        ignore_order: bool,
        validate_processed_bytes: bool,
    ):
        return PipeChecker(
            request["endpoint_url"],
            self.pipe_name,
            checker_pipe_name,
            token,
            only_response_times,
            ignore_order,
            validate_processed_bytes,
        )

    def _delta_percentage(self, checker: float, current: float) -> float:
        try:
            return round(((checker - current) / current) * 100, 2)
        except Exception as exc:
            logging.warning(f"Error calculating delta: {exc}")
            return 0.0

    def run_pipe_checker(
        self,
        pipe_requests_to_check: List[Dict[str, str]],
        checker_pipe_name: str,
        token: str,
        only_response_times: bool,
        ignore_order: bool,
        validate_processed_bytes: bool,
        failfast: bool,
        custom_output: bool = False,
    ) -> PipeCheckerRunnerResponse:
        class PipeCheckerTextTestResult(unittest.TextTestResult):
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                self.custom_output = kwargs.pop("custom_output", False)
                super(PipeCheckerTextTestResult, self).__init__(*args, **kwargs)
                self.success: List[PipeChecker] = []

            def addSuccess(self, test: PipeChecker):  # type: ignore
                super(PipeCheckerTextTestResult, self).addSuccess(test)
                self.success.append(test)

            def startTest(self, test):
                if not self.custom_output:
                    super(PipeCheckerTextTestResult, self).startTest(test)
                else:
                    super(unittest.TextTestResult, self).startTest(test)

            def _write_status(self, test, status):
                if self.custom_output:
                    self.stream.write(status.upper())
                    self.stream.write(" - ")
                    self.stream.write(str(test))
                    self.stream.write(" - ")
                    self.stream.writeln(test._write_performance())

                else:
                    self.stream.writeln(status)
                self.stream.flush()
                self._newline = True

        suite = unittest.TestSuite()

        for _, request in enumerate(pipe_requests_to_check):
            suite.addTest(
                self._get_checker(
                    request, checker_pipe_name, token, only_response_times, ignore_order, validate_processed_bytes
                )
            )

        result = PipeCheckerTextTestResult(
            self.checker_stream_result_class(sys.stdout), descriptions=True, verbosity=2, custom_output=custom_output
        )
        result.failfast = failfast
        suite.run(result)

        metrics_summary: Optional[Dict[str, Any]] = None
        metrics_timing: Dict[str, Tuple[float, float, float]] = {}

        try:
            current_response_times: List[float] = []
            checker_response_times: List[float] = []

            current_read_bytes: List[int] = []
            checker_read_bytes: List[int] = []
            if result.success:
                for test in result.success:
                    current_response_times.append(test.current_response_time)
                    checker_response_times.append(test.checker_response_time)

                    current_read_bytes.append(test.current_read_bytes)
                    checker_read_bytes.append(test.checker_read_bytes)

                for test, _ in result.failures:  # type: ignore
                    current_response_times.append(test.current_response_time)
                    checker_response_times.append(test.checker_response_time)

                    current_read_bytes.append(test.current_read_bytes)
                    checker_read_bytes.append(test.checker_read_bytes)

            metrics_summary = {
                "run": result.testsRun,
                "passed": len(result.success),
                "failed": len(result.failures),
                "percentage_passed": len(result.success) * 100 / result.testsRun,
                "percentage_failed": len(result.failures) * 100 / result.testsRun,
            }
            metrics_timing = {
                "min response time": (
                    min(current_response_times),
                    min(checker_response_times),
                    self._delta_percentage(min(checker_response_times), min(current_response_times)),
                ),
                "max response time": (
                    max(current_response_times),
                    max(checker_response_times),
                    self._delta_percentage(max(checker_response_times), max(current_response_times)),
                ),
                "mean response time": (
                    float(format(mean(current_response_times), ".6f")),
                    float(format(mean(checker_response_times), ".6f")),
                    self._delta_percentage(
                        float(format(mean(checker_response_times), ".6f")),
                        float(format(mean(current_response_times), ".6f")),
                    ),
                ),
                "median response time": (
                    median(current_response_times),
                    median(checker_response_times),
                    self._delta_percentage(median(checker_response_times), median(current_response_times)),
                ),
                "p90 response time": (
                    sorted(current_response_times)[math.ceil(len(current_response_times) * 0.9) - 1],
                    sorted(checker_response_times)[math.ceil(len(checker_response_times) * 0.9) - 1],
                    self._delta_percentage(
                        sorted(checker_response_times)[math.ceil(len(checker_response_times) * 0.9) - 1],
                        sorted(current_response_times)[math.ceil(len(current_response_times) * 0.9) - 1],
                    ),
                ),
                "min read bytes": (
                    format_size(min(current_read_bytes)),
                    format_size(min(checker_read_bytes)),
                    self._delta_percentage(min(checker_read_bytes), min(current_read_bytes)),
                ),
                "max read bytes": (
                    format_size(max(current_read_bytes)),
                    format_size(max(checker_read_bytes)),
                    self._delta_percentage(max(checker_read_bytes), max(current_read_bytes)),
                ),
                "mean read bytes": (
                    format_size(mean(current_read_bytes)),
                    format_size(mean(checker_read_bytes)),
                    self._delta_percentage(mean(checker_read_bytes), mean(current_read_bytes)),
                ),
                "median read bytes": (
                    format_size(median(current_read_bytes)),
                    format_size(median(checker_read_bytes)),
                    self._delta_percentage(median(checker_read_bytes), median(current_read_bytes)),
                ),
                "p90 read bytes": (
                    format_size(sorted(current_read_bytes)[math.ceil(len(current_read_bytes) * 0.9) - 1]),
                    format_size(sorted(checker_read_bytes)[math.ceil(len(checker_read_bytes) * 0.9) - 1]),
                    self._delta_percentage(
                        sorted(checker_read_bytes)[math.ceil(len(checker_read_bytes) * 0.9) - 1],
                        sorted(current_read_bytes)[math.ceil(len(current_read_bytes) * 0.9) - 1],
                    ),
                ),
            }
        except Exception:
            pass

        failures = []
        if not result.wasSuccessful():
            for _test, err in result.failures:
                try:
                    i = err.index("AssertionError") + len("AssertionError :")
                    failures.append({"name": str(_test), "error": err[i:]})
                except Exception:
                    pass

        return PipeCheckerRunnerResponse(
            pipe_name=checker_pipe_name,
            test_type=getattr(self, "test_type", ""),
            output=getattr(result.stream, "_buffer", ""),
            metrics_summary=metrics_summary,
            metrics_timing=metrics_timing,
            failed=failures,
            was_successfull=result.wasSuccessful(),
        )


async def check_pipe(
    pipe,
    host: str,
    token: str,
    populate: bool,
    cl: TinyB,
    limit: int = 0,
    sample_by_params: int = 0,
    only_response_times=False,
    matches: Optional[List[str]] = None,
    failfast: bool = False,
    validate_processed_bytes: bool = False,
    ignore_order: bool = False,
    token_for_requests_to_check: Optional[str] = None,
    current_pipe: Optional[Dict[str, Any]] = None,
):
    checker_pipe = deepcopy(pipe)
    checker_pipe["name"] = f"{checker_pipe['name']}__checker"

    if current_pipe:
        pipe_type = current_pipe["type"]
        if pipe_type == PipeTypes.COPY:
            await cl.pipe_remove_copy(current_pipe["id"], current_pipe["copy_node"])
        if pipe_type == PipeTypes.DATA_SINK:
            await cl.pipe_remove_sink(current_pipe["id"], current_pipe["sink_node"])

    # In case of doing --force for a materialized view, checker is being created as standard pipe
    for node in checker_pipe["nodes"]:
        node["params"]["type"] = PipeNodeTypes.STANDARD

    if populate:
        raise Exception(FeedbackManager.error_check_pipes_populate())

    runner = PipeCheckerRunner(pipe["name"], host)
    headers = (
        {"Authorization": f"Bearer {token_for_requests_to_check}"}
        if token_for_requests_to_check
        else {"Authorization": f"Bearer {token}"}
    )

    sql_for_coverage, sql_latest_requests = runner.get_sqls_for_requests_to_check(
        matches or [], sample_by_params, limit
    )

    params = {"q": sql_for_coverage if limit == 0 and sample_by_params > 0 else sql_latest_requests}
    r: requests.Response = await requests_get(f"{host}/v0/sql?{urlencode(params)}", headers=headers)

    # If we get a timeout, fallback to just the last requests

    if not r or r.status_code == 408:
        params = {"q": sql_latest_requests}
        r = await requests_get(f"{host}/v0/sql?{urlencode(params)}", headers=headers)

    if not r or r.status_code != 200:
        raise Exception(FeedbackManager.error_check_pipes_api(pipe=pipe["name"]))

    pipe_requests_to_check: List[Dict[str, str]] = []
    for x in r.json().get("data", []):
        pipe_requests_to_check += [{"endpoint_url": f"{host}{request}"} for request in x["endpoint_url"]]

    # Let's query if there are no results from tinybird.pipe_stats_rt
    if not pipe_requests_to_check:
        headers = (
            {"Authorization": f"Bearer {token_for_requests_to_check}"}
            if token_for_requests_to_check
            else {"Authorization": f"Bearer {token}"}
        )
        r = await requests_get(f"{host}/v0/pipes/{pipe['name']}/requests", headers=headers)
        if r.status_code != 200:
            raise Exception(FeedbackManager.error_check_pipes_api(pipe=pipe["name"]))
        pipe_requests_to_check = r.json().get("requests", {}).get("top", [])
        if matches:
            requests_filter = []
            for request in pipe_requests_to_check:
                if all([request["endpoint_url"].find(match) != -1 for match in matches]):
                    requests_filter.append(request)
            pipe_requests_to_check = requests_filter

        pipe_requests_to_check = pipe_requests_to_check[:limit]

    if not pipe_requests_to_check:
        return

    await new_pipe(checker_pipe, cl, force=True, check=False, populate=populate)

    runner_response = runner.run_pipe_checker(
        pipe_requests_to_check,
        checker_pipe["name"],
        token,
        only_response_times,
        ignore_order,
        validate_processed_bytes,
        failfast,
    )

    try:
        if runner_response.metrics_summary and runner_response.metrics_timing:
            column_names = ["Timing Metric (s)", "Current", "New"]

            click.echo("\n==== Test Metrics ====\n")
            click.echo(
                format_pretty_table(
                    [
                        [
                            runner_response.metrics_summary["run"],
                            runner_response.metrics_summary["passed"],
                            runner_response.metrics_summary["failed"],
                            runner_response.metrics_summary["percentage_passed"],
                            runner_response.metrics_summary["percentage_failed"],
                        ]
                    ],
                    column_names=["Test Run", "Test Passed", "Test Failed", "% Test Passed", "% Test Failed"],
                )
            )

            click.echo("\n==== Response Time Metrics ====\n")
            click.echo(
                format_pretty_table(
                    [
                        [metric, runner_response.metrics_timing[metric][0], runner_response.metrics_timing[metric][1]]
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
    except Exception:
        pass

    if not runner_response.was_successfull:
        for failure in runner_response.failed:
            try:
                click.echo("==== Test FAILED ====\n")
                click.echo(failure["name"])
                click.echo(FeedbackManager.error_check_pipe(error=failure["error"]))
                click.echo("=====================\n\n\n")
            except Exception:
                pass
        raise RuntimeError("Invalid results, you can bypass checks by running push with the --no-check flag")

    # Only delete if no errors, so we can check results after failure
    headers = {"Authorization": f"Bearer {token}"}
    r = await requests_delete(f"{host}/v0/pipes/{checker_pipe['name']}", headers=headers)
    if r.status_code != 204:
        click.echo(FeedbackManager.warning_check_pipe(content=r.content))


async def check_materialized(pipe, host, token, cl, override_datasource=False, current_pipe=None):
    checker_pipe = deepcopy(pipe)
    checker_pipe["name"] = f"{checker_pipe['name']}__checker"
    headers = {"Authorization": f"Bearer {token}"}

    if current_pipe:
        from_copy_to_materialized = current_pipe["type"] == "copy"
        if from_copy_to_materialized:
            await cl.pipe_remove_copy(current_pipe["id"], current_pipe["copy_node"])

    materialized_node = None
    for node in checker_pipe["nodes"]:
        if node["params"]["type"] == "materialized":
            materialized_node = deepcopy(node)
            materialized_node["params"]["override_datasource"] = "true" if override_datasource else "false"
        node["params"]["type"] = "standard"

    try:
        pipe_created = False
        await new_pipe(
            checker_pipe, cl, force=True, check=False, populate=False, skip_tokens=True, ignore_sql_errors=False
        )
        pipe_created = True
        response = await cl.analyze_pipe_node(checker_pipe["name"], materialized_node, dry_run="true")
        if response.get("warnings"):
            show_materialized_view_warnings(response["warnings"])

    except Exception as e:
        raise click.ClickException(FeedbackManager.error_while_check_materialized(error=str(e)))
    finally:
        if pipe_created:
            r = await requests_delete(f"{host}/v0/pipes/{checker_pipe['name']}", headers=headers)
            if r.status_code != 204:
                click.echo(FeedbackManager.warning_check_pipe(content=r.content))


async def check_copy_pipe(pipe, copy_node, tb_client: TinyB):
    target_datasource = copy_node["params"].get("target_datasource", None)
    if not target_datasource:
        raise CLIPipeException(FeedbackManager.error_creating_copy_pipe_target_datasource_required())

    try:
        await tb_client.get_datasource(target_datasource)
    except DoesNotExistException:
        raise CLIPipeException(
            FeedbackManager.error_creating_copy_pipe_target_datasource_not_found(target_datasource=target_datasource)
        )
    except Exception as e:
        raise CLIPipeException(FeedbackManager.error_exception(error=e))

    schedule_cron = copy_node["params"].get("copy_schedule", None)
    is_valid_cron = not schedule_cron or (
        schedule_cron and (schedule_cron == "@on-demand" or croniter.is_valid(schedule_cron))
    )

    if not is_valid_cron:
        raise CLIPipeException(FeedbackManager.error_creating_copy_pipe_invalid_cron(schedule_cron=schedule_cron))

    if not pipe:
        return

    pipe_name = pipe["name"]
    pipe_type = pipe["type"]

    if pipe_type == PipeTypes.ENDPOINT:
        await tb_client.pipe_remove_endpoint(pipe_name, pipe["endpoint"])

    if pipe_type == PipeTypes.DATA_SINK:
        await tb_client.pipe_remove_sink(pipe_name, pipe["sink_node"])


async def check_sink_pipe(pipe, sink_node, tb_client: TinyB):
    if not sink_node["export_params"]:
        return

    if not pipe:
        return

    pipe_name = pipe["name"]
    pipe_type = pipe["type"]

    schedule_cron = sink_node["export_params"].get("schedule_cron", "")
    is_valid_cron = not schedule_cron or (schedule_cron and croniter.is_valid(schedule_cron))

    if not is_valid_cron:
        raise CLIPipeException(FeedbackManager.error_creating_sink_pipe_invalid_cron(schedule_cron=schedule_cron))

    if pipe_type == PipeTypes.ENDPOINT:
        await tb_client.pipe_remove_endpoint(pipe_name, pipe["endpoint"])

    if pipe_type == PipeTypes.COPY:
        await tb_client.pipe_remove_copy(pipe_name, pipe["copy_node"])


def show_materialized_view_warnings(warnings):
    """
    >>> show_materialized_view_warnings([{'code': 'SIM', 'weight': 1}])

    >>> show_materialized_view_warnings([{'code': 'SIM', 'weight': 1}, {'code': 'HUGE_JOIN', 'weight': 2}, {'text': "Column 'number' is present in the GROUP BY but not in the SELECT clause. This might indicate a not valid Materialized View, please make sure you aggregate and GROUP BY in the topmost query.", 'code': 'GROUP_BY', 'weight': 100, 'documentation': 'https://tinybird.co/docs/guides/materialized-views.html#use-the-same-alias-in-select-and-group-by'}])
    ⚠️  Column 'number' is present in the GROUP BY but not in the SELECT clause. This might indicate a not valid Materialized View, please make sure you aggregate and GROUP BY in the topmost query. For more information read https://tinybird.co/docs/guides/materialized-views.html#use-the-same-alias-in-select-and-group-by or contact us at support@tinybird.co
    >>> show_materialized_view_warnings([{'code': 'SINGLE_JOIN', 'weight': 300}, {'text': "Column 'number' is present in the GROUP BY but not in the SELECT clause. This might indicate a not valid Materialized View, please make sure you aggregate and GROUP BY in the topmost query.", 'code': 'GROUP_BY', 'weight': 100, 'documentation': 'https://tinybird.co/docs/guides/materialized-views.html#use-the-same-alias-in-select-and-group-by'}])
    ⚠️  Column 'number' is present in the GROUP BY but not in the SELECT clause. This might indicate a not valid Materialized View, please make sure you aggregate and GROUP BY in the topmost query. For more information read https://tinybird.co/docs/guides/materialized-views.html#use-the-same-alias-in-select-and-group-by or contact us at support@tinybird.co
    """
    excluded_warnings = ["SIM", "SIM_UNKNOWN", "HUGE_JOIN"]
    sorted_warnings = sorted(warnings, key=lambda warning: warning["weight"])
    most_important_warning = {}
    for warning in sorted_warnings:
        if warning.get("code") and warning["code"] not in excluded_warnings:
            most_important_warning = warning
            break
    if most_important_warning:
        click.echo(
            FeedbackManager.single_warning_materialized_pipe(
                content=most_important_warning["text"], docs_url=most_important_warning["documentation"]
            )
        )


async def get_token_from_main_branch(branch_tb_client: TinyB) -> Optional[str]:
    token_from_main_branch = None
    current_workspace = await branch_tb_client.workspace_info()
    # current workspace is a branch
    if current_workspace.get("main"):
        response = await branch_tb_client.user_workspaces()
        workspaces = response["workspaces"]
        prod_workspace = next(
            (workspace for workspace in workspaces if workspace["id"] == current_workspace["main"]), None
        )
        if prod_workspace:
            token_from_main_branch = prod_workspace.get("token")
    return token_from_main_branch


async def new_pipe(
    p,
    tb_client: TinyB,
    force: bool = False,
    check: bool = True,
    populate: bool = False,
    populate_subset=None,
    populate_condition=None,
    unlink_on_populate_error: bool = False,
    wait_populate: bool = False,
    skip_tokens: bool = False,
    tag: str = "",
    ignore_sql_errors: bool = False,
    only_response_times: bool = False,
    timeout=None,
    run_tests: bool = False,
    as_standard: bool = False,
    tests_to_run: int = 0,
    tests_to_sample_by_params: int = 0,
    tests_filter_by: Optional[List[str]] = None,
    tests_failfast: bool = False,
    tests_ignore_order: bool = False,
    tests_validate_processed_bytes: bool = False,
    override_datasource: bool = False,
    tests_check_requests_from_branch: bool = False,
    config: Any = None,
    fork_downstream: Optional[bool] = False,
):  # noqa: C901
    # TODO use tb_client instead of calling the urls directly.
    host = tb_client.host
    token = tb_client.token

    headers = {"Authorization": f"Bearer {token}"}

    if tag:
        tag = tag + "__"

    cli_params = {}
    cli_params["cli_version"] = tb_client.version
    cli_params["description"] = p.get("description", "")
    cli_params["ignore_sql_errors"] = "true" if ignore_sql_errors else "false"

    r: requests.Response = await requests_get(f"{host}/v0/pipes/{p['name']}?{urlencode(cli_params)}", headers=headers)

    current_pipe = r.json() if r.status_code == 200 else None
    pipe_exists = current_pipe is not None

    is_materialized = any([node.get("params", {}).get("type", None) == "materialized" for node in p["nodes"]])
    copy_node = next((node for node in p["nodes"] if node.get("params", {}).get("type", None) == "copy"), None)
    sink_node = next((node for node in p["nodes"] if node.get("params", {}).get("type", None) == "sink"), None)

    if pipe_exists:
        if force or run_tests:
            # TODO: this should create a different node and rename it to the final one on success
            if check and not populate:
                if not is_materialized and not copy_node and not sink_node:
                    await check_pipe(
                        p,
                        host,
                        token,
                        populate,
                        tb_client,
                        only_response_times=only_response_times,
                        limit=tests_to_run,
                        sample_by_params=tests_to_sample_by_params,
                        matches=tests_filter_by,
                        failfast=tests_failfast,
                        validate_processed_bytes=tests_validate_processed_bytes,
                        ignore_order=tests_ignore_order,
                        token_for_requests_to_check=await get_token_from_main_branch(tb_client)
                        if not tests_check_requests_from_branch
                        else None,
                        current_pipe=current_pipe,
                    )
                else:
                    if is_materialized:
                        await check_materialized(
                            p,
                            host,
                            token,
                            tb_client,
                            override_datasource=override_datasource,
                            current_pipe=current_pipe,
                        )
                    if copy_node:
                        await check_copy_pipe(pipe=current_pipe, copy_node=copy_node, tb_client=tb_client)
                    if sink_node:
                        await check_sink_pipe(pipe=current_pipe, sink_node=sink_node, tb_client=tb_client)
            if run_tests:
                logging.info(f"skipping force override of {p['name']}")
                return
        else:
            raise click.ClickException(FeedbackManager.error_pipe_already_exists(pipe=p["name"]))
    elif not pipe_exists and check:
        if is_materialized:
            await check_materialized(
                p, host, token, tb_client, override_datasource=override_datasource, current_pipe=current_pipe
            )
        if copy_node:
            await check_copy_pipe(pipe=current_pipe, copy_node=copy_node, tb_client=tb_client)

    params = {}
    params.update(cli_params)
    if force:
        params["force"] = "true"
    if populate:
        params["populate"] = "true"
    if populate_condition:
        params["populate_condition"] = populate_condition
    if populate_subset:
        params["populate_subset"] = populate_subset
    params["unlink_on_populate_error"] = "true" if unlink_on_populate_error else "false"
    params["branch_mode"] = "fork" if fork_downstream else "None"

    body = {"name": p["name"], "description": p.get("description", "")}

    def parse_node(node):
        if "params" in node:
            node.update(node["params"])
            if node.get("type", "") == "materialized" and override_datasource:
                node["override_datasource"] = "true"
            del node["params"]
        return node

    if p["nodes"]:
        body["nodes"] = [parse_node(n) for n in p["nodes"]]

    if copy_node:
        body["target_datasource"] = copy_node.get("target_datasource", None)
        # We will update the schedule cron later
        body["schedule_cron"] = None

    if sink_node:
        body.update(sink_node.get("export_params", {}))

    post_headers = {"Content-Type": "application/json"}

    post_headers.update(headers)

    try:
        data = await tb_client._req(
            f"/v0/pipes?{urlencode(params)}", method="POST", headers=post_headers, data=json.dumps(body)
        )
    except Exception as e:
        raise Exception(FeedbackManager.error_pushing_pipe(pipe=p["name"], error=str(e)))

    datasource = data.get("datasource", None)
    created_datasource = data.get("created_datasource", None)

    if datasource and created_datasource:
        if copy_node:
            click.echo(FeedbackManager.info_copy_datasource_created(pipe=p["name"], datasource=datasource["name"]))
        else:
            click.echo(
                FeedbackManager.info_materialized_datasource_created(pipe=p["name"], datasource=datasource["name"])
            )
    elif datasource and not created_datasource:
        if copy_node:
            click.echo(FeedbackManager.info_copy_datasource_used(pipe=p["name"], datasource=datasource["name"]))
        else:
            click.echo(FeedbackManager.info_materialized_datasource_used(pipe=p["name"], datasource=datasource["name"]))

    if datasource and populate:
        job_url = data.get("job", {}).get("job_url", None)
        job_id = data.get("job", {}).get("job_id", None)
        if populate_subset:
            click.echo(FeedbackManager.info_populate_subset_job_url(url=job_url, subset=populate_subset))
        elif populate_condition:
            click.echo(
                FeedbackManager.info_populate_condition_job_url(url=job_url, populate_condition=populate_condition)
            )
        else:
            click.echo(FeedbackManager.info_populate_job_url(url=job_url))

        if wait_populate:
            await wait_job(tb_client, job_id, job_url, "Populating", timeout)
    else:
        if data.get("type") == "default" and not skip_tokens and not as_standard and not copy_node and not sink_node:
            # FIXME: set option to add last node as endpoint in the API
            endpoint_node = next(
                (node for node in data.get("nodes", []) if node.get("type") == "endpoint"), data.get("nodes", [])[-1]
            )
            try:
                data = await tb_client._req(
                    f"/v0/pipes/{p['name']}/nodes/{endpoint_node.get('id')}/endpoint?{urlencode(cli_params)}",
                    method="POST",
                    headers=headers,
                )
            except Exception as e:
                raise Exception(
                    FeedbackManager.error_creating_endpoint(
                        node=endpoint_node.get("name"), pipe=p["name"], error=str(e)
                    )
                )

            click.echo(FeedbackManager.success_test_endpoint_no_token(host=host, pipe=p["name"]))

    if copy_node:
        pipe_id = data["id"]
        node = next((node for node in data["nodes"] if node["node_type"] == "copy"), None)
        if node:
            copy_params = {"pipe_name_or_id": pipe_id, "node_id": node["id"]}
            try:
                target_datasource = copy_node.get("target_datasource", None)
                schedule_cron = copy_node.get("copy_schedule", None)
                schedule_cron = None if schedule_cron == "@on-demand" else schedule_cron
                current_target_datasource_id = data["copy_target_datasource"]
                target_datasource_response = await tb_client.get_datasource(target_datasource)
                target_datasource_to_send = (
                    target_datasource
                    if target_datasource_response.get("id", target_datasource) != current_target_datasource_id
                    else None
                )
                copy_params["target_datasource"] = target_datasource_to_send
                current_schedule = data.get("schedule", {})
                current_schedule_cron = current_schedule.get("cron", None) if current_schedule else None
                schedule_cron_should_be_removed = current_schedule_cron and not schedule_cron
                copy_params["schedule_cron"] = "None" if schedule_cron_should_be_removed else schedule_cron
                await tb_client.pipe_update_copy(**copy_params)
            except Exception as e:
                raise Exception(
                    FeedbackManager.error_setting_copy_node(node=copy_node.get("name"), pipe=p["name"], error=str(e))
                )

    if p["tokens"] and not skip_tokens and not as_standard and data.get("type") == "endpoint":
        # search for token with specified name and adds it if not found or adds permissions to it
        t = None
        for tk in p["tokens"]:
            token_name = tag + tk["token_name"]
            t = await tb_client.get_token_by_name(token_name)
            if t:
                break
        if not t:
            token_name = tag + tk["token_name"]
            click.echo(FeedbackManager.info_create_not_found_token(token=token_name))
            try:
                r = await tb_client.create_token(token_name, f"PIPES:{tk['permissions']}:{p['name']}", "P", p["name"])
                token = r["token"]  # type: ignore
            except Exception as e:
                raise Exception(FeedbackManager.error_creating_pipe(error=e))
        else:
            click.echo(FeedbackManager.info_create_found_token(token=token_name))
            scopes = [f"PIPES:{tk['permissions']}:{p['name']}"]
            for x in t["scopes"]:
                sc = x["type"] if "resource" not in x else f"{x['type']}:{x['resource']}"
                scopes.append(sc)
            try:
                r = await tb_client.alter_tokens(token_name, scopes)
                token = r["token"]  # type: ignore
            except Exception as e:
                raise Exception(FeedbackManager.error_creating_pipe(error=e))
        click.echo(FeedbackManager.success_test_endpoint(host=host, pipe=p["name"], token=token))


async def share_and_unshare_datasource(
    client: TinyB,
    datasource: Dict[str, Any],
    user_token: str,
    workspaces_current_shared_with: List[str],
    workspaces_to_share: List[str],
    current_ws: Optional[Dict[str, Any]],
) -> None:
    datasource_name = datasource.get("name", "")
    datasource_id = datasource.get("id", "")
    workspaces: List[Dict[str, Any]]

    # In case we are pushing to an enviroment, we don't share the datasource
    # FIXME: Have only once way to get the current workspace
    if current_ws:
        # Force to get all the workspaces the user can access
        workspace = current_ws
        workspaces = (await client.user_workspaces()).get("workspaces", [])
    else:
        workspace = await client.user_workspace_branches()
        workspaces = workspace.get("workspaces", [])

    if workspace.get("is_branch", False):
        click.echo(FeedbackManager.info_skipping_sharing_datasources_environment(datasource=datasource["name"]))
        return

    # We duplicate the client to use the user_token
    user_client: TinyB = deepcopy(client)
    user_client.token = user_token
    if not workspaces_current_shared_with:
        for workspace_to_share in workspaces_to_share:
            w: Optional[Dict[str, Any]] = next((w for w in workspaces if w["name"] == workspace_to_share), None)
            if not w:
                raise Exception(
                    f"Unable to share datasource with the workspace {workspace_to_share}. Review that you have the admin permissions on this workspace"
                )

            await user_client.datasource_share(
                datasource_id=datasource_id,
                current_workspace_id=workspace.get("id", ""),
                destination_workspace_id=w.get("id", ""),
            )
            click.echo(
                FeedbackManager.success_datasource_shared(datasource=datasource_name, workspace=w.get("name", ""))
            )
    else:
        shared_with = [
            w
            for w in workspaces
            if next((ws for ws in workspaces_current_shared_with if ws == w["id"] or ws == w["name"]), None)
        ]
        defined_to_share_with = [
            w for w in workspaces if next((ws for ws in workspaces_to_share if ws == w["id"] or ws == w["name"]), None)
        ]
        workspaces_need_to_share = [w for w in defined_to_share_with if w not in shared_with]
        workspaces_need_to_unshare = [w for w in shared_with if w not in defined_to_share_with]

        for w in workspaces_need_to_share:
            await user_client.datasource_share(
                datasource_id=datasource_id,
                current_workspace_id=workspace.get("id", ""),
                destination_workspace_id=w.get("id", ""),
            )
            click.echo(
                FeedbackManager.success_datasource_shared(datasource=datasource["name"], workspace=w.get("name", ""))
            )

        for w in workspaces_need_to_unshare:
            await user_client.datasource_unshare(
                datasource_id=datasource_id,
                current_workspace_id=workspace.get("id", ""),
                destination_workspace_id=w.get("id", ""),
            )
            click.echo(
                FeedbackManager.success_datasource_unshared(datasource=datasource_name, workspace=w.get("name", ""))
            )


async def new_ds(
    ds: Dict[str, Any],
    client: TinyB,
    user_token: Optional[str],
    force: bool = False,
    skip_confirmation: bool = False,
    current_ws=None,
    fork_downstream: Optional[bool] = False,
):
    ds_name = ds["params"]["name"]

    async def manage_tokens():
        # search for token with specified name and adds it if not found or adds permissions to it
        t = None
        for tk in ds["tokens"]:
            token_name = tk["token_name"]
            t = await client.get_token_by_name(token_name)
            if t:
                break
        if not t:
            token_name = tk["token_name"]
            click.echo(FeedbackManager.info_create_not_found_token(token=token_name))
            # DS == token_origin.Origins.DATASOURCE
            await client.create_token(token_name, f"DATASOURCES:{tk['permissions']}:{ds_name}", "DS", ds_name)
        else:
            click.echo(FeedbackManager.info_create_found_token(token=token_name))
            scopes = [f"DATASOURCES:{tk['permissions']}:{ds_name}"]
            for x in t["scopes"]:
                sc = x["type"] if "resource" not in x else f"{x['type']}:{x['resource']}"
                scopes.append(sc)
            await client.alter_tokens(token_name, scopes)

    try:
        existing_ds = await client.get_datasource(ds_name)
        datasource_exists = True
    except DoesNotExistException:
        datasource_exists = False

    if not datasource_exists or fork_downstream:
        params = ds["params"]
        params["branch_mode"] = "fork" if fork_downstream else "None"

        try:
            if params.get("service") == "s3" and params.get("connector") and params.get("bucket_uri"):
                data = await client.preview_s3_bucket(params["connector"], params["bucket_uri"])
                if data:
                    files = data.get("files", [])
                    if len(files) > 0:
                        file_name = files[0].get("name", "")
                        extension = file_name.split(".")[-1]
                        valid_formats = ["csv", "ndjson", "parquet"]
                        if extension not in valid_formats:
                            raise Exception(
                                FeedbackManager.error_format(extension=extension, valid_formats=valid_formats)
                            )
                        params["format"] = extension

            datasource = (await client.datasource_create_from_definition(params)).get("datasource", {})
            if "tokens" in ds and ds["tokens"]:
                await manage_tokens()

            if "shared_with" in ds and ds["shared_with"]:
                if not user_token:
                    click.echo(FeedbackManager.info_skipping_shared_with_entry())
                else:
                    await share_and_unshare_datasource(
                        client,
                        datasource,
                        user_token,
                        workspaces_current_shared_with=[],
                        workspaces_to_share=ds["shared_with"],
                        current_ws=current_ws,
                    )

        except Exception as e:
            raise Exception(FeedbackManager.error_creating_datasource(error=str(e)))
        return

    if not force:
        raise click.ClickException(FeedbackManager.error_datasource_already_exists(datasource=ds_name))

    if ds.get("shared_with", []) or existing_ds.get("shared_with", []):
        if not user_token:
            click.echo(FeedbackManager.info_skipping_shared_with_entry())
        else:
            await share_and_unshare_datasource(
                client,
                existing_ds,
                user_token,
                existing_ds.get("shared_with", []),
                ds.get("shared_with", []),
                current_ws,
            )

    alter_response = None
    alter_error_message = None
    new_description = None
    new_schema = None
    new_ttl = None

    try:
        if datasource_exists and ds["params"]["description"] != existing_ds["description"]:
            new_description = ds["params"]["description"]

        if datasource_exists and ds["params"].get("engine_ttl") != existing_ds["engine"].get("ttl"):
            new_ttl = ds["params"].get("engine_ttl", "false")

        # Schema fixed by the kafka connector
        if datasource_exists and (
            ds["params"]["schema"].replace(" ", "") != existing_ds["schema"]["sql_schema"].replace(" ", "")
        ):
            new_schema = ds["params"]["schema"]
        if new_description or new_schema or new_ttl and not fork_downstream:
            alter_response = await client.alter_datasource(
                ds_name, new_schema=new_schema, description=new_description, ttl=new_ttl, dry_run=True
            )
    except Exception as e:
        if "There were no operations to perform" in str(e):
            pass
        else:
            alter_error_message = str(e)

    if alter_response:
        click.echo(FeedbackManager.info_datasource_doesnt_match(datasource=ds_name))
        for operation in alter_response["operations"]:
            click.echo(f"**   -  {operation}")

        if skip_confirmation:
            make_changes = True
        else:
            make_changes = click.prompt(FeedbackManager.info_ask_for_alter_confirmation()).lower() == "y"

        if make_changes:
            await client.alter_datasource(
                ds_name, new_schema=new_schema, description=new_description, ttl=new_ttl, dry_run=False
            )
            click.echo(FeedbackManager.success_datasource_alter())
            return
        else:
            alter_error_message = "Alter datasource cancelled"

    connector_data = None
    promote_error_message = None

    ds_params = ds["params"]
    service = ds_params.get("service")
    DATASOURCE_VALID_SERVICES_TO_UPDATE = ["bigquery", "snowflake"]
    DATASOURCE_INVALID_SERVICES_TO_UPDATE = ["s3"]
    if (
        datasource_exists
        and service
        and service in [*DATASOURCE_VALID_SERVICES_TO_UPDATE, *DATASOURCE_INVALID_SERVICES_TO_UPDATE]
    ):
        connector_required_params = {
            "bigquery": ["service", "cron", "external_data_source"],
            "snowflake": ["connector", "service", "cron", "external_data_source"],
            "s3": ["connector", "service", "cron", "bucket_uri"],
        }.get(service, [])

        if not all(key in ds_params for key in connector_required_params):
            return

        connector = ds_params.get("connector", None)

        if service in DATASOURCE_INVALID_SERVICES_TO_UPDATE:
            connector_id = existing_ds.get("connector", "")
            if not connector_id:
                return

            current_connector = await client.get_connector_by_id(existing_ds.get("connector", ""))
            if not current_connector:
                return

            if current_connector["name"] != ds_params["connection"]:
                param = "connection"
                datafile_param = ImportReplacements.get_datafile_param_for_linker_param(service, param) or param
                raise Exception(FeedbackManager.error_updating_connector_not_supported(param=datafile_param))

            linkers = current_connector.get("linkers", [])
            linker = next((linker for linker in linkers if linker["datasource_id"] == existing_ds["id"]), None)
            if not linker:
                return

            linker_settings = linker.get("settings", {})
            for param, value in linker_settings.items():
                ds_params_value = ds_params.get(param, None)
                if ds_params_value and ds_params_value != value:
                    datafile_param = ImportReplacements.get_datafile_param_for_linker_param(service, param) or param
                    raise Exception(
                        FeedbackManager.error_updating_connector_not_supported(param=datafile_param.upper())
                    )
            return

        connector_data = {
            "connector": connector,
            "service": service,
            "cron": ds_params.get("cron", None),
            "external_data_source": ds_params.get("external_data_source", None),
            "bucket_uri": ds_params.get("bucket_uri", None),
            "mode": ds_params.get("mode", "replace"),
            "query": ds_params.get("query", None),
            "ingest_now": ds_params.get("ingest_now", False),
        }

        try:
            await client.promote_datasource(ds_name, connector_data)
            click.echo(FeedbackManager.success_promoting_datasource(datasource=ds_name))
            return
        except Exception as e:
            promote_error_message = str(e)

    # removed replacing by default. When a datasource is removed data is
    # removed and all the references needs to be updated
    if (
        os.getenv("TB_I_KNOW_WHAT_I_AM_DOING")
        and click.prompt(FeedbackManager.info_ask_for_datasource_confirmation()) == ds_name
    ):  # TODO move to CLI
        try:
            await client.datasource_delete(ds_name)
            click.echo(FeedbackManager.success_delete_datasource(datasource=ds_name))
        except Exception:
            raise Exception(FeedbackManager.error_removing_datasource(datasource=ds_name))
        return
    else:
        if alter_error_message:
            raise click.ClickException(
                FeedbackManager.error_datasource_already_exists_and_alter_failed(
                    datasource=ds_name, alter_error_message=alter_error_message
                )
            )
        if promote_error_message:
            raise click.ClickException(
                FeedbackManager.error_promoting_datasource(datasource=ds_name, error=promote_error_message)
            )
        else:
            click.echo(FeedbackManager.warning_datasource_already_exists(datasource=ds_name))


async def new_token(token: Dict[str, Any], client: TinyB, force: bool = False):
    existing_token = None
    try:
        existing_token = await client.token_get(token["name"])
    except Exception:
        pass

    if not existing_token:
        await client.token_create(token)
        return

    if force:
        ADMIN_SCOPES = ["ADMIN", "ADMIN_USER"]
        if any([scope["type"] in ADMIN_SCOPES for scope in existing_token["scopes"]]):
            raise click.ClickException(FeedbackManager.error_token_cannot_be_overriden(token=token["name"]))

        await client.token_update(token)
        return

    raise click.ClickException(FeedbackManager.error_token_already_exists(token=token["name"]))


async def exec_file(
    config: Optional[Dict[str, Any]],
    r: Dict[str, Any],
    tb_client: TinyB,
    force: bool,
    check: bool,
    debug: bool,
    populate: bool,
    populate_subset,
    populate_condition,
    unlink_on_populate_error,
    wait_populate,
    tag,
    user_token: Optional[str],
    override_datasource: bool = False,
    ignore_sql_errors: bool = False,
    skip_confirmation: bool = False,
    only_response_times: bool = False,
    timeout=None,
    run_tests=False,
    as_standard=False,
    tests_to_run: int = 0,
    tests_to_sample_by_params: int = 0,
    tests_filter_by: Optional[List[str]] = None,
    tests_failfast: bool = False,
    tests_ignore_order: bool = False,
    tests_validate_processed_bytes: bool = False,
    tests_check_requests_from_branch: bool = False,
    current_ws: Optional[Dict[str, Any]] = None,
    fork_downstream: Optional[bool] = False,
):
    if debug:
        click.echo(FeedbackManager.debug_running_file(file=pp.pformat(r)))
    if r["resource"] == "pipes":
        await new_pipe(
            r,
            tb_client,
            force,
            check,
            populate,
            populate_subset,
            populate_condition,
            unlink_on_populate_error,
            wait_populate,
            tag=tag,
            ignore_sql_errors=ignore_sql_errors,
            only_response_times=only_response_times,
            timeout=timeout,
            run_tests=run_tests,
            as_standard=as_standard,
            tests_to_run=tests_to_run,
            tests_to_sample_by_params=tests_to_sample_by_params,
            tests_filter_by=tests_filter_by,
            tests_failfast=tests_failfast,
            tests_ignore_order=tests_ignore_order,
            tests_validate_processed_bytes=tests_validate_processed_bytes,
            override_datasource=override_datasource,
            tests_check_requests_from_branch=tests_check_requests_from_branch,
            fork_downstream=fork_downstream,
        )
    elif r["resource"] == "datasources":
        await new_ds(
            r,
            tb_client,
            user_token,
            force,
            skip_confirmation=skip_confirmation,
            current_ws=current_ws,
            fork_downstream=fork_downstream,
        )
    elif r["resource"] == "tokens":
        await new_token(r, tb_client, force)
    else:
        raise Exception(FeedbackManager.error_unknown_resource(resource=r["resource"]))


def get_name_tag_version(ds: str, ignore_prefix: bool) -> Dict[str, Any]:
    """
    Given a name like "name__dev__v0" returns ['name', 'dev', 'v0']
    >>> get_name_tag_version('dev__name__v0', False)
    {'name': 'name', 'tag': 'dev', 'version': 0}
    >>> get_name_tag_version('name__v0', False)
    {'name': 'name', 'tag': None, 'version': 0}
    >>> get_name_tag_version('dev__name', False)
    {'name': 'name', 'tag': 'dev', 'version': None}
    >>> get_name_tag_version('name', False)
    {'name': 'name', 'tag': None, 'version': None}
    >>> get_name_tag_version('horario__3__pipe', False)
    {'name': '3__pipe', 'tag': 'horario', 'version': None}
    >>> get_name_tag_version('horario__checker', False)
    {'name': 'horario__checker', 'tag': None, 'version': None}
    >>> get_name_tag_version('dev__horario__checker', False)
    {'name': 'horario__checker', 'tag': 'dev', 'version': None}
    >>> get_name_tag_version('tg__dActividades__v0_pipe_3907', False)
    {'name': 'dActividades', 'tag': 'tg', 'version': 0}
    >>> get_name_tag_version('tg__dActividades__va_pipe_3907', False)
    {'name': 'dActividades__va_pipe_3907', 'tag': 'tg', 'version': None}
    >>> get_name_tag_version('tg__origin_workspace.shared_ds__v3907', False)
    {'name': 'origin_workspace.shared_ds', 'tag': 'tg', 'version': 3907}
    >>> get_name_tag_version('tmph8egtl__', False)
    {'name': 'tmph8egtl__', 'tag': None, 'version': None}
    >>> get_name_tag_version('tmph8egtl__123__', False)
    {'name': 'tmph8egtl__123__', 'tag': None, 'version': None}
    >>> get_name_tag_version('dev__name__v0', True)
    {'name': 'dev__name', 'tag': None, 'version': 0}
    >>> get_name_tag_version('name__v0', True)
    {'name': 'name', 'tag': None, 'version': 0}
    >>> get_name_tag_version('dev__name', True)
    {'name': 'dev__name', 'tag': None, 'version': None}
    >>> get_name_tag_version('name', True)
    {'name': 'name', 'tag': None, 'version': None}
    >>> get_name_tag_version('horario__3__pipe', True)
    {'name': 'horario__3__pipe', 'tag': None, 'version': None}
    >>> get_name_tag_version('horario__checker', True)
    {'name': 'horario__checker', 'tag': None, 'version': None}
    >>> get_name_tag_version('dev__horario__checker', True)
    {'name': 'dev__horario__checker', 'tag': None, 'version': None}
    >>> get_name_tag_version('tg__dActividades__v0_pipe_3907', True)
    {'name': 'tg__dActividades', 'tag': None, 'version': 0}
    >>> get_name_tag_version('tg__dActividades__va_pipe_3907', True)
    {'name': 'tg__dActividades__va_pipe_3907', 'tag': None, 'version': None}
    >>> get_name_tag_version('tg__origin_workspace.shared_ds__v3907', True)
    {'name': 'tg__origin_workspace.shared_ds', 'tag': None, 'version': 3907}
    >>> get_name_tag_version('tmph8egtl__', True)
    {'name': 'tmph8egtl__', 'tag': None, 'version': None}
    >>> get_name_tag_version('tmph8egtl__123__', True)
    {'name': 'tmph8egtl__123__', 'tag': None, 'version': None}
    """
    tk = ds.rsplit("__", 2)
    if len(tk) == 1:
        return {"name": tk[0], "tag": None, "version": None}
    elif len(tk) == 2:
        if len(tk[1]):
            if tk[1][0] == "v" and re.match("[0-9]+$", tk[1][1:]):
                return {"name": tk[0], "tag": None, "version": int(tk[1][1:])}
            else:
                if tk[1] == "checker" or ignore_prefix:
                    return {"name": tk[0] + "__" + tk[1], "tag": None, "version": None}
                return {"name": tk[1], "tag": tk[0], "version": None}
    elif len(tk) == 3 and len(tk[2]):
        if tk[2] == "checker":
            if ignore_prefix:
                return {"name": tk[0] + "__" + tk[1] + "__" + tk[2], "tag": None, "version": None}
            return {"name": tk[1] + "__" + tk[2], "tag": tk[0], "version": None}
        if tk[2][0] == "v":
            parts = tk[2].split("_")
            try:
                if ignore_prefix:
                    return {"name": tk[0] + "__" + tk[1], "tag": None, "version": int(parts[0][1:])}
                return {"name": tk[1], "tag": tk[0], "version": int(parts[0][1:])}
            except ValueError:
                if ignore_prefix:
                    return {"name": tk[0] + "__" + tk[1] + "__" + tk[2], "tag": None, "version": None}
                return {"name": f"{tk[1]}__{tk[2]}", "tag": tk[0], "version": None}
        else:
            if ignore_prefix:
                return {"name": "__".join(tk[0:]), "tag": None, "version": None}
            return {"name": "__".join(tk[1:]), "tag": tk[0], "version": None}

    return {"name": ds, "tag": None, "version": None}


def get_resource_versions(datasources: List[str]):
    """
    return the latest version for all the datasources
    """
    versions = {}
    for x in datasources:
        t = get_name_tag_version(x, ignore_prefix=False)
        name = t["name"]
        if t["tag"]:
            name = f"{t['tag']}__{name}"
        if t.get("version", None) is not None:
            versions[name] = t["version"]
    return versions


def get_remote_resource_name_without_version(remote_resource_name: str) -> str:
    """
    >>> get_remote_resource_name_without_version("r__datasource")
    'r__datasource'
    >>> get_remote_resource_name_without_version("r__datasource__v0")
    'r__datasource'
    >>> get_remote_resource_name_without_version("datasource")
    'datasource'
    """
    parts = get_name_tag_version(remote_resource_name, ignore_prefix=False)
    if parts["tag"]:
        return parts["tag"] + "__" + parts["name"]
    else:
        return parts["name"]


def get_dep_from_raw_tables(x: str) -> str:
    """
    datasources KEY command generates tables, this transform the used table with the source file
    >>> get_dep_from_raw_tables('test')
    'test'
    >>> get_dep_from_raw_tables('test_join_by_column')
    'test'
    """

    try:
        return x[: x.index("_join_by_")]
    except ValueError:
        return x


async def build_graph(
    filenames: Iterable[str],
    tb_client: TinyB,
    dir_path: Optional[str] = None,
    tag: Optional[str] = "",
    resource_versions=None,
    workspace_map: Optional[Dict] = None,
    process_dependencies: bool = False,
    verbose: bool = False,
    skip_connectors: bool = False,
    workspace_lib_paths: Optional[List[Tuple[str, str]]] = None,
    current_ws: Optional[Dict[str, Any]] = None,
    changed: Optional[Dict[str, Any]] = None,
    only_changes: bool = False,
    fork_downstream: Optional[bool] = False,
    is_internal: Optional[bool] = False,
):  # noqa: C901 B006
    """process files"""
    to_run: Dict[str, Any] = {}
    deps: List[str] = []
    dep_map: Dict[str, Any] = {}
    embedded_datasources = {}
    if not workspace_map:
        workspace_map = {}

    all_dep_map = dict()
    deps_tag = ""

    if tag:
        deps_tag = f"{tag}__"

    if dir_path is None:
        dir_path = os.getcwd()

    if process_dependencies and only_changes:
        all_resources, all_dep_map = await build_graph(
            get_project_filenames(dir_path),
            tb_client,
            dir_path=dir_path,
            tag=tag,
            process_dependencies=True,
            resource_versions=resource_versions,
            workspace_map=workspace_map,
            skip_connectors=True,
            workspace_lib_paths=workspace_lib_paths,
            current_ws=current_ws,
            changed=None,
            only_changes=False,
            is_internal=is_internal,
        )

    async def process(
        filename: str,
        deps,
        dep_map: Dict[str, Any],
        to_run: Dict[str, Any],
        workspace_lib_paths: Optional[List[Tuple[str, str]]],
        deps_tag: str,
    ):
        name, kind = filename.rsplit(".", 1)

        try:
            res = await process_file(
                filename,
                tb_client,
                tag,
                resource_versions=resource_versions,
                skip_connectors=skip_connectors,
                workspace_map=workspace_map,
                workspace_lib_paths=workspace_lib_paths,
                current_ws=current_ws,
            )
        except click.ClickException as e:
            raise e
        except Exception as e:
            raise click.ClickException(str(e))

        for r in res:
            fn = r["resource_name"]
            if changed and fn in changed and (not changed[fn] or changed[fn] in ["shared", "remote"]):
                continue
            to_run[fn] = r
            file_deps = r.get("deps", [])
            deps += file_deps
            # calculate and look for deps
            dep_list = []
            for x in file_deps:
                if x not in INTERNAL_TABLES or is_internal:
                    f, ds = find_file_by_name(
                        dir_path, x, verbose, workspace_lib_paths=workspace_lib_paths, resource=r, deps_tag=deps_tag
                    )
                    if f:
                        dep_list.append(deps_tag + f.rsplit(".", 1)[0])
                    if ds:
                        ds_fn = ds["resource_name"]
                        prev = to_run.get(ds_fn, {})
                        to_run[ds_fn] = deepcopy(r)
                        try:
                            to_run[ds_fn]["deps"] = list(
                                set(to_run[ds_fn].get("deps", []) + prev.get("deps", []) + [fn.replace(deps_tag, "")])
                            )
                        except ValueError:
                            pass
                        embedded_datasources[x] = to_run[ds_fn]
                    else:
                        e_ds = embedded_datasources.get(x, None)
                        if e_ds:
                            dep_list.append(e_ds["resource_name"])

            # In case the datasource is to be shared and we have mapping, let's replace the name
            if "shared_with" in r and workspace_map:
                mapped_workspaces: List[str] = []
                for shared_with in r["shared_with"]:
                    mapped_workspaces.append(
                        workspace_map.get(shared_with)
                        if workspace_map.get(shared_with, None) is not None
                        else shared_with
                    )
                r["shared_with"] = mapped_workspaces

            dep_map[fn] = set(dep_list)
        return os.path.basename(name)

    processed = set()

    async def get_processed(filenames: Iterable[str]):
        for filename in filenames:
            resource = Path(filename).resolve().stem
            if changed and resource in changed and (not changed[resource] or changed[resource] in ["shared", "remote"]):
                continue
            if os.path.isdir(filename):
                await get_processed(filenames=get_project_filenames(filename))
            else:
                if verbose:
                    click.echo(FeedbackManager.info_processing_file(filename=filename))

                if ".incl" in filename:
                    click.echo(FeedbackManager.warning_skipping_include_file(file=filename))

                name = await process(filename, deps, dep_map, to_run, workspace_lib_paths, deps_tag)
                processed.add(name)

    await get_processed(filenames=filenames)

    if process_dependencies:
        if only_changes:
            for key in dict(to_run):
                # look for deps that are the target data source of a materialized node
                target_datasource = get_target_materialized_data_source_name(to_run[key])
                if target_datasource:
                    # look in all_dep_map items that have as a dependency the target data source and are an endpoint
                    for _key, deps in all_dep_map.items():
                        for dep in deps:
                            if (
                                dep == target_datasource
                                or (dep == key and target_datasource not in all_dep_map.get(key, []))
                            ) and is_endpoint_with_no_dependencies(
                                all_resources.get(_key, {}), all_dep_map, all_resources
                            ):
                                dep_map[_key] = deps
                                to_run[_key] = all_resources.get(_key)
        else:
            while len(deps) > 0:
                dep = deps.pop()
                if dep not in processed:
                    processed.add(dep)
                    f = full_path_by_name(dir_path, dep, workspace_lib_paths)
                    if f:
                        if verbose:
                            try:
                                processed_filename = f.relative_to(os.getcwd())
                            except ValueError:
                                processed_filename = f
                            click.echo(FeedbackManager.info_processing_file(filename=processed_filename))
                        await process(str(f), deps, dep_map, to_run, workspace_lib_paths, deps_tag)

    def create_downstream_dependency_graph(dependency_graph, all_resources):
        """
        This function reverses the dependency graph obtained from build_graph so you have downstream dependencies for each node in the graph.

        Additionally takes into account target_datasource of materialized views
        """
        downstream_dependency_graph = {node: set() for node in dependency_graph}

        for node, dependencies in dependency_graph.items():
            for dependency in dependencies:
                downstream_dependency_graph[dependency].add(node)

        for key in dict(downstream_dependency_graph):
            target_datasource = get_target_materialized_data_source_name(all_resources[key])
            if target_datasource:
                downstream_dependency_graph[key].update({target_datasource})
                try:
                    downstream_dependency_graph[target_datasource].remove(key)
                except KeyError:
                    pass

        return downstream_dependency_graph

    def update_dep_map_recursively(dep_map, downstream_dep_map, all_resources, to_run, key, external_visitor):
        """
        Given a downstream_dep_map obtained from create_downstream_dependency_graph this function updates each node recursively to complete the downstream dependency graph for each node
        """
        if key not in dep_map:
            dep_map[key] = set()
        elif key in external_visitor:
            return
        else:
            external_visitor.add(key)

        for dep in downstream_dep_map.get(key, {}):
            if dep not in downstream_dep_map:
                continue
            to_run[dep] = all_resources.get(dep)
            update_dep_map_recursively(dep_map, downstream_dep_map, all_resources, to_run, dep, external_visitor)
            dep_map[key].update(downstream_dep_map[dep])
            dep_map[key].update({dep})
            try:
                dep_map[key].remove(key)
            except KeyError:
                return

        to_run[key] = all_resources.get(key)

    new_dep_map = dep_map
    if all_dep_map and fork_downstream:
        downstream_dep_map = create_downstream_dependency_graph(all_dep_map, all_resources)
        new_dep_map = {}
        external_visitor: Set[str] = set()
        for key in list(dep_map.keys()):
            update_dep_map_recursively(new_dep_map, downstream_dep_map, all_resources, to_run, key, external_visitor)

    return to_run, new_dep_map


async def get_changes_from_main(
    only_changes: bool,
    client: TinyB,
    config: Optional[Dict[str, Any]] = None,
    current_ws: Optional[Dict[str, Any]] = None,
    filenames: Optional[List[str]] = None,
):
    changed = None
    if not only_changes:
        return changed

    if current_ws and not current_ws.get("is_branch"):
        changed = await diff_command(filenames, True, client, no_color=True, with_print=False)
    elif config and config.get("host"):
        workspace = await get_current_main_workspace(client, config)

        if workspace:
            ws_client = TinyB(workspace["token"], config["host"], version=VERSION)
            changed = await diff_command(filenames, True, ws_client, no_color=True, with_print=False)
    return changed


def get_project_filenames(folder: str) -> List[str]:
    folders: List[str] = [
        f"{folder}/*.datasource",
        f"{folder}/datasources/*.datasource",
        f"{folder}/*.pipe",
        f"{folder}/pipes/*.pipe",
        f"{folder}/endpoints/*.pipe",
        f"{folder}/*.token",
        f"{folder}/tokens/*.token",
    ]
    filenames: List[str] = []
    for x in folders:
        filenames += glob.glob(x)
    return filenames


async def folder_push(
    tb_client: TinyB,
    tag: str = "",
    filenames: Optional[List[str]] = None,
    dry_run: bool = False,
    check: bool = False,
    push_deps: bool = False,
    only_changes: bool = False,
    git_release: bool = False,
    debug: bool = False,
    force: bool = False,
    override_datasource: bool = False,
    folder: str = ".",
    populate: bool = False,
    populate_subset=None,
    populate_condition: Optional[str] = None,
    unlink_on_populate_error: bool = False,
    upload_fixtures: bool = False,
    wait: bool = False,
    ignore_sql_errors: bool = False,
    skip_confirmation: bool = False,
    only_response_times: bool = False,
    workspace_map=None,
    workspace_lib_paths=None,
    no_versions: bool = False,
    timeout=None,
    run_tests: bool = False,
    as_standard: bool = False,
    raise_on_exists: bool = False,
    verbose: bool = True,
    tests_to_run: int = 0,
    tests_sample_by_params: int = 0,
    tests_filter_by: Optional[List[str]] = None,
    tests_failfast: bool = False,
    tests_ignore_order: bool = False,
    tests_validate_processed_bytes: bool = False,
    tests_check_requests_from_branch: bool = False,
    config: Optional[Dict[str, Any]] = None,
    user_token: Optional[str] = None,
    fork_downstream: Optional[bool] = False,
    is_internal: Optional[bool] = False,
):  # noqa: C901
    workspaces: List[Dict[str, Any]] = (await tb_client.user_workspaces_and_branches()).get("workspaces", [])
    current_ws: Dict[str, Any] = next(
        (workspace for workspace in workspaces if config and workspace.get("id", ".") == config.get("id", "..")), {}
    )
    is_environment = current_ws.get("is_branch", False)

    if not workspace_map:
        workspace_map = {}
    if not workspace_lib_paths:
        workspace_lib_paths = []

    workspace_lib_paths = list(workspace_lib_paths)
    # include vendor libs without overriding user ones
    existing_workspaces = set(x[1] for x in workspace_lib_paths)
    vendor_path = Path("vendor")
    if vendor_path.exists():
        for x in vendor_path.iterdir():
            if x.is_dir() and x.name not in existing_workspaces:
                workspace_lib_paths.append((x.name, x))

    datasources: List[Dict[str, Any]] = await tb_client.datasources()
    pipes: List[Dict[str, Any]] = await tb_client.pipes()

    existing_resources: List[str] = [x["name"] for x in datasources] + [x["name"] for x in pipes]
    # replace workspace mapping names
    for old_ws, new_ws in workspace_map.items():
        existing_resources = [re.sub(f"^{old_ws}\.", f"{new_ws}.", x) for x in existing_resources]

    if not no_versions:
        resource_versions = get_resource_versions(existing_resources)
    else:
        resource_versions = {}

    remote_resource_names = [get_remote_resource_name_without_version(x) for x in existing_resources]

    # replace workspace mapping names
    for old_ws, new_ws in workspace_map.items():
        remote_resource_names = [re.sub(f"^{old_ws}\.", f"{new_ws}.", x) for x in remote_resource_names]

    if not filenames:
        filenames = get_project_filenames(folder)

    # get the list of changes comparing to the main branch
    if git_release:
        current_release = current_ws.get("release")
        if not current_release:
            raise CLIGitReleaseException(FeedbackManager.error_init_release(workspace=current_ws["name"]))
        cli_git_release = CLIGitRelease()
        cli_git_release.validate_local_for_release(current_release)
        diffs = cli_git_release.diff_datafiles(current_release["commit"])
        click.echo(
            FeedbackManager.info_git_release_diffs(
                workspace=current_ws["name"],
                current_release_commit=current_release["commit"],
                new_release_commit=cli_git_release.head_commit(),
            )
        )
        for d in diffs:
            click.echo(cli_git_release.ChangeType(d.change_type).as_feedback_message(d))
        changed = cli_git_release.get_changes_from_diffs(diffs, filenames)
    else:
        # get the list of changes comparing to the main branch
        changed = (
            await get_changes_from_main(only_changes, tb_client, config, current_ws, filenames=filenames)
            if config
            else None
        )

    # build graph to get new versions for all the files involved in the query
    # dependencies need to be processed always to get the versions
    resources, dep_map = await build_graph(
        filenames,
        tb_client,
        dir_path=folder,
        tag=tag,
        process_dependencies=True,
        workspace_map=workspace_map,
        skip_connectors=True,
        workspace_lib_paths=workspace_lib_paths,
        current_ws=current_ws,
        changed=changed,
        only_changes=only_changes or git_release,
        fork_downstream=fork_downstream,
        is_internal=is_internal,
    )

    # update existing versions
    if not no_versions:
        latest_datasource_versions = resource_versions.copy()

        for dep in resources.values():
            ds = dep["resource_name"]
            if dep["version"] is not None:
                latest_datasource_versions[ds] = dep["version"]
    else:
        latest_datasource_versions = {}

    # build the graph again with the right version
    to_run, dep_map = await build_graph(
        filenames,
        tb_client,
        dir_path=folder,
        tag=tag,
        resource_versions=latest_datasource_versions,
        workspace_map=workspace_map,
        process_dependencies=push_deps,
        verbose=verbose,
        workspace_lib_paths=workspace_lib_paths,
        current_ws=current_ws,
        changed=changed,
        only_changes=only_changes or git_release,
        skip_connectors=is_environment,
        fork_downstream=fork_downstream,
        is_internal=is_internal,
    )

    if debug:
        pp.pprint(to_run)

    if verbose:
        click.echo(FeedbackManager.info_building_dependencies())

    def should_push_file() -> bool:
        """
        Function to know if we need to run a file or not
        """
        if name not in remote_resource_names:
            return True
        # When we need to try to push a file when it doesn't exist and the version is different that the existing one
        resource_full_name = (
            f"{name}__v{latest_datasource_versions.get(name)}" if name in latest_datasource_versions else name
        )
        if resource_full_name not in existing_resources:
            return True
        if force or run_tests:
            return True
        return False

    async def push(
        name: str,
        to_run: Dict[str, Any],
        resource_versions: Dict[str, Any],
        latest_datasource_versions: Dict[str, Any],
        dry_run: bool,
        fork_downstream: Optional[bool] = False,
    ):
        if name in to_run:
            if not dry_run:
                if should_push_file():
                    if name not in resource_versions:
                        version = ""
                        if name in latest_datasource_versions:
                            version = f"(v{latest_datasource_versions[name]})"
                        click.echo(FeedbackManager.info_processing_new_resource(name=name, version=version))
                    else:
                        click.echo(
                            FeedbackManager.info_processing_resource(
                                name=name,
                                version=latest_datasource_versions[name],
                                latest_version=resource_versions.get(name),
                            )
                        )
                    try:
                        await exec_file(
                            config,
                            to_run[name],
                            tb_client,
                            force,
                            check,
                            debug and verbose,
                            populate,
                            populate_subset,
                            populate_condition,
                            unlink_on_populate_error,
                            wait,
                            tag,
                            user_token,
                            override_datasource,
                            ignore_sql_errors,
                            skip_confirmation,
                            only_response_times,
                            timeout,
                            run_tests,
                            as_standard,
                            tests_to_run,
                            tests_sample_by_params,
                            tests_filter_by,
                            tests_failfast,
                            tests_ignore_order,
                            tests_validate_processed_bytes,
                            tests_check_requests_from_branch,
                            current_ws,
                            fork_downstream,
                        )
                        if not run_tests:
                            click.echo(
                                FeedbackManager.success_create(
                                    name=name
                                    if to_run[name]["version"] is None
                                    else f'{name}__v{to_run[name]["version"]}'
                                )
                            )
                    except Exception as e:
                        exception = FeedbackManager.error_push_file_exception(
                            filename=to_run[name]["filename"], error=e
                        )
                        raise click.ClickException(exception)
                else:
                    if raise_on_exists:
                        raise AlreadyExistsException(
                            FeedbackManager.warning_name_already_exists(
                                name=name if to_run[name]["version"] is None else f'{name}__v{to_run[name]["version"]}'
                            )
                        )
                    else:
                        click.echo(
                            FeedbackManager.warning_name_already_exists(
                                name=name if to_run[name]["version"] is None else f'{name}__v{to_run[name]["version"]}'
                            )
                        )
            else:
                if (
                    name not in remote_resource_names
                    or resource_versions.get(name.replace(".", "_"), "") != latest_datasource_versions.get(name, "")
                    or force
                ):
                    if name not in resource_versions:
                        version = ""
                        if name in latest_datasource_versions:
                            version = f"(v{latest_datasource_versions[name]})"
                        click.echo(FeedbackManager.info_dry_processing_new_resource(name=name, version=version))
                    else:
                        click.echo(
                            FeedbackManager.info_dry_processing_resource(
                                name=name,
                                version=latest_datasource_versions[name],
                                latest_version=resource_versions.get(name),
                            )
                        )
                else:
                    click.echo(FeedbackManager.warning_dry_name_already_exists(name=name))

    endpoints_dep_map = dict()
    pipes_dep_map = dict()
    processed = set()

    groups = [group for group in toposort(dep_map)]
    for group in groups:
        for name in group:
            # https://gitlab.com/tinybird/analytics/-/merge_requests/6737
            if is_endpoint_with_no_dependencies(to_run.get(name, {}), dep_map, to_run):
                endpoints_dep_map[name] = dep_map[name]
                continue
            # FIXME: name in dep_map?? that's wrong it should be there
            if fork_downstream and not is_datasource(to_run.get(name)) and name in dep_map:
                pipes_dep_map[name] = dep_map[name]
                continue
            await push(name, to_run, resource_versions, latest_datasource_versions, dry_run, fork_downstream)
            processed.add(name)

    if fork_downstream:
        for group in toposort(pipes_dep_map):
            for name in group:
                if name not in processed:
                    await push(name, to_run, resource_versions, latest_datasource_versions, dry_run, fork_downstream)

    # push endpoints with no dependencies or dependencies with other endpoints
    for group in toposort(endpoints_dep_map):
        for name in group:
            if name not in processed:
                await push(name, to_run, resource_versions, latest_datasource_versions, dry_run, fork_downstream)

    if not dry_run and git_release:
        # Update workspace release
        release = await cli_git_release.update_release(tb_client, current_ws)
        click.echo(FeedbackManager.success_git_release(release_commit=release["commit"]))

    if not dry_run and not run_tests:
        if upload_fixtures:
            click.echo(FeedbackManager.info_pushing_fixtures())

            # We need to upload the fixtures even if there is no change
            if is_environment:
                to_run, dep_map = await build_graph(
                    filenames,
                    tb_client,
                    dir_path=folder,
                    tag=tag,
                    resource_versions=latest_datasource_versions,
                    workspace_map=workspace_map,
                    process_dependencies=push_deps,
                    verbose=verbose,
                    workspace_lib_paths=workspace_lib_paths,
                    current_ws=current_ws,
                    skip_connectors=is_environment,
                )

            processed = set()
            for group in toposort(dep_map):
                for f in group:
                    name = os.path.basename(f)
                    if name not in processed:
                        if name in to_run:
                            await check_fixtures_data(
                                tb_client,
                                to_run[name],
                                debug,
                                folder,
                                force,
                                mode="append" if is_environment else "replace",
                            )
                            processed.add(name)
            for f in to_run:
                if f not in processed:
                    await check_fixtures_data(
                        tb_client, to_run[f], debug, folder, force, mode="append" if is_environment else "replace"
                    )
        else:
            if verbose:
                click.echo(FeedbackManager.info_not_pushing_fixtures())

    return to_run


async def check_fixtures_data(
    cl: TinyB, r: Dict[str, Any], debug: bool, folder: str = "", force: bool = False, mode: str = "replace"
):
    if debug:
        click.echo(FeedbackManager.info_checking_file(file=pp.pformat(r)))
    if r["resource"] in ["pipes", "tokens"]:
        pass
    elif r["resource"] == "datasources":
        datasource_name = r["params"]["name"]
        name = os.path.basename(r["filename"]).rsplit(".", 1)[0]
        csv_test_file = Path(folder) / "fixtures" / f"{name}.csv"

        if not csv_test_file.exists():
            csv_test_file = Path(folder) / "datasources" / "fixtures" / f"{name}.csv"
        if not csv_test_file.exists():
            csv_test_file = Path(folder) / "datasources" / "fixtures" / f"{name}.ndjson"
        if csv_test_file.exists():
            # Let's validate only when when we are going to replace the actual data
            result = await cl.query(sql=f"SELECT count() as c FROM {datasource_name} FORMAT JSON")
            count = result["data"][0]["c"]

            if count > 0 and not force:
                raise click.ClickException(
                    FeedbackManager.error_push_fixture_will_replace_data(datasource=datasource_name)
                )

            click.echo(
                FeedbackManager.info_checking_file_size(
                    filename=r["filename"], size=sizeof_fmt(os.stat(csv_test_file).st_size)
                )
            )
            sys.stdout.flush()
            try:
                await cl.datasource_append_data(
                    datasource_name=r["params"]["name"], file=csv_test_file, mode=mode, format=csv_test_file.suffix[1:]
                )
                click.echo(FeedbackManager.success_processing_data())
            except Exception as e:
                raise click.ClickException(FeedbackManager.error_processing_blocks(error=e))

        else:
            click.echo(FeedbackManager.warning_file_not_found(name=csv_test_file))
    else:
        raise Exception(FeedbackManager.error_unknown_resource(resource=r["resource"]))


DATAFILE_NEW_LINE = "\n"
DATAFILE_INDENT = " " * 4


def format_schema(file_parts: List[str], node: Dict[str, Any]) -> List[str]:
    file_parts.append("SCHEMA >")
    file_parts.append(DATAFILE_NEW_LINE)
    columns = schema_to_sql_columns(node["columns"])
    file_parts.append(f",{DATAFILE_NEW_LINE}".join(map(lambda x: f"    {x}", columns)))
    file_parts.append(DATAFILE_NEW_LINE)
    file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_data_connector(file_parts: List[str], node: Dict[str, Any]) -> List[str]:
    ll = len(file_parts)
    [file_parts.append(f"{k.upper()} {v}{DATAFILE_NEW_LINE}") for k, v in node.items() if "kafka" in k]  # type: ignore
    if ll < len(file_parts):
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_import_settings(file_parts: List[str], node: Dict[str, Any]) -> List[str]:
    ll = len(file_parts)
    [file_parts.append(f"{k.upper()} {v}{DATAFILE_NEW_LINE}") for k, v in node.items() if "import_" in k]  # type: ignore
    if ll < len(file_parts):
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_include(file_parts: List[str], doc: Datafile, unroll_includes: bool = False) -> List[str]:
    if unroll_includes:
        return file_parts

    assert doc.raw is not None

    include = [line for line in doc.raw if "INCLUDE" in line and ".incl" in line]
    if len(include):
        file_parts.append(include[0])
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


async def format_datasource(
    filename: str, unroll_includes: bool = False, for_diff: bool = False, client: Optional[TinyB] = None
) -> str:
    doc: Datafile = parse_datasource(filename)
    file_parts: List[str] = []
    if for_diff:
        is_kafka = "kafka_connection_name" in doc.nodes[0]
        if is_kafka:
            kafka_metadata_columns = [
                "__value",
                "__headers",
                "__topic",
                "__partition",
                "__offset",
                "__timestamp",
                "__key",
            ]
            columns = [c for c in doc.nodes[0]["columns"] if c["name"] not in kafka_metadata_columns]
            doc.nodes[0].update(
                {
                    "columns": columns,
                }
            )
        format_version(file_parts, doc)
        format_tokens(file_parts, doc)
        format_schema(file_parts, doc.nodes[0])
        await format_engine(file_parts, doc.nodes[0], only_ttl=True, client=client)
        format_shared_with(file_parts, doc)
    else:
        format_sources(file_parts, doc)
        format_maintainer(file_parts, doc)
        format_version(file_parts, doc)
        format_description(file_parts, doc)
        format_tokens(file_parts, doc)
        format_schema(file_parts, doc.nodes[0])
        await format_engine(file_parts, doc.nodes[0])
        format_include(file_parts, doc, unroll_includes=unroll_includes)
        format_data_connector(file_parts, doc.nodes[0])
        format_import_settings(file_parts, doc.nodes[0])
        format_shared_with(file_parts, doc)
    result = "".join(file_parts)
    result = result.rstrip("\n") + "\n"
    return result


def format_version(file_parts: List[str], doc: Datafile) -> List[str]:
    version = doc.version if doc.version is not None else ""
    if version != "":
        file_parts.append(f"VERSION {version}")
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_maintainer(file_parts: List[str], doc: Datafile) -> List[str]:
    maintainer = doc.maintainer if doc.maintainer is not None else ""
    if maintainer:
        file_parts.append(f"MAINTAINER {maintainer}")
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_sources(file_parts: List[str], doc: Datafile) -> List[str]:
    for source in doc.sources:
        file_parts.append(f"SOURCE {source}")
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_description(file_parts: List[str], doc: Any) -> List[str]:
    description = doc.description if doc.description is not None else ""
    if description:
        file_parts.append("DESCRIPTION >")
        file_parts.append(DATAFILE_NEW_LINE)
        [file_parts.append(f"{DATAFILE_INDENT}{d.strip()}\n") for d in description.split(DATAFILE_NEW_LINE) if d.strip()]  # type: ignore
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_tokens(file_parts: List[str], doc: Datafile) -> List[str]:
    for token in doc.tokens:
        file_parts.append(f'TOKEN "{token["token_name"]}" {token["permissions"]}')
        file_parts.append(DATAFILE_NEW_LINE)
    if len(doc.tokens):
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_node_sql(file_parts: List[str], node: Dict[str, Any], line_length: Optional[int] = None) -> List[str]:
    file_parts.append("SQL >")
    file_parts.append(DATAFILE_NEW_LINE)
    file_parts.append(format_sql(node["sql"], DATAFILE_INDENT, line_length=line_length))
    file_parts.append(DATAFILE_NEW_LINE)
    file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_shared_with(file_parts: List[str], doc: Datafile) -> List[str]:
    if doc.shared_with:
        file_parts.append("SHARED_WITH >")
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append("\n".join([f"{DATAFILE_INDENT}{workspace_name}" for workspace_name in doc.shared_with]))
    return file_parts


async def format_engine(
    file_parts: List[str], node: Dict[str, Any], only_ttl: bool = False, client: Optional[TinyB] = None
) -> List[str]:
    if only_ttl:
        if node.get("engine", None):
            for arg in sorted(node["engine"].get("args", [])):
                if arg[0].upper() == "TTL":
                    elem = ", ".join([x.strip() for x in arg[1].split(",")])
                    try:
                        if client:
                            ttl_sql = await client.sql_get_format(f"select {elem}", with_clickhouse_format=True)
                            formatted_ttl = ttl_sql[7:]
                        else:
                            formatted_ttl = elem
                    except Exception:
                        formatted_ttl = elem
                    file_parts.append(f"ENGINE_{arg[0].upper()} {formatted_ttl}")
                    file_parts.append(DATAFILE_NEW_LINE)
            file_parts.append(DATAFILE_NEW_LINE)
        return file_parts
    else:
        if node.get("engine", None):
            empty = '""'
            file_parts.append(f'ENGINE {node["engine"]["type"]}' if node.get("engine", {}).get("type") else empty)
            file_parts.append(DATAFILE_NEW_LINE)
            for arg in sorted(node["engine"].get("args", [])):
                elem = ", ".join([x.strip() for x in arg[1].split(",")])
                file_parts.append(f"ENGINE_{arg[0].upper()} {elem if elem else empty}")
                file_parts.append(DATAFILE_NEW_LINE)
            file_parts.append(DATAFILE_NEW_LINE)
        return file_parts


async def format_node_type(file_parts: List[str], node: Dict[str, Any]) -> List[str]:
    if node.get("type", "").lower() == PipeNodeTypes.MATERIALIZED:
        file_parts.append(f'TYPE {node["type"].upper()}')
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(f'DATASOURCE {node["datasource"]}')
        file_parts.append(DATAFILE_NEW_LINE)
        await format_engine(file_parts, node)
    if ExportReplacements.is_export_node(node):
        file_parts.append(f'TYPE {node["type"].upper()}')
        export_params = ExportReplacements.get_params_from_datafile(node)
        file_parts.append(DATAFILE_NEW_LINE)
        for param, value in export_params.items():
            if param == "schedule_cron" and not value:
                value = "@on-demand"
            datafile_key = ExportReplacements.get_datafile_key(param)
            if datafile_key:
                file_parts.append(f"{datafile_key} {value}")
                file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_pipe_include(file_parts: List[str], node: Dict[str, Any], includes: Dict[str, Any]) -> List[str]:
    if includes:
        for k, v in includes.copy().items():
            if node["name"] in v:
                file_parts.append(f"INCLUDE {k}")
                file_parts.append(DATAFILE_NEW_LINE)
                file_parts.append(DATAFILE_NEW_LINE)
                del includes[k]
    return file_parts


async def format_node(
    file_parts: List[str],
    node: Dict[str, Any],
    includes: Dict[str, Any],
    line_length: Optional[int] = None,
    unroll_includes: bool = False,
) -> None:
    if not unroll_includes:
        format_pipe_include(file_parts, node, includes)
    item = [k for k, _ in includes.items() if node["name"].strip() in k]
    if item and not unroll_includes:
        return

    file_parts.append(f'NODE {node["name"].strip()}')
    file_parts.append(DATAFILE_NEW_LINE)

    from collections import namedtuple

    Doc = namedtuple("Doc", ["description"])
    format_description(file_parts, Doc(node.get("description", "")))
    format_node_sql(file_parts, node, line_length=line_length)
    await format_node_type(file_parts, node)


async def format_pipe(filename: str, line_length: Optional[int], unroll_includes: bool = False) -> str:
    doc = parse_pipe(filename)

    file_parts: List[str] = []
    format_sources(file_parts, doc)
    format_maintainer(file_parts, doc)
    format_version(file_parts, doc)
    format_description(file_parts, doc)
    format_tokens(file_parts, doc)
    if doc.includes and not unroll_includes:
        for k in doc.includes:
            # We filter only the include files as we currently have 2 items for each include
            # { 'include_file.incl': 'First node of the include" }
            # { 'first node of the pipe after the include': }
            if ".incl" not in k:
                continue

            # We get all the nodes inside the include and remove them from the unrolled pipe as we want things unrolled
            include_parameters = _unquote(k)

            # If they use an include with parameters like `INCLUDE "xxx.incl" "GROUP_COL=path" "MATERIALIZED_VIEW=speed_insights_path_daily_mv"``
            # We just want the file name to take nodes
            include_file = include_parameters.split('"')[0]
            include_file = (
                Path(os.path.dirname(filename)) / eval_var(include_file)
                if "." in include_file
                else eval_var(include_file)
            )
            included_pipe = parse_pipe(include_file)
            pipe_nodes = doc.nodes.copy()
            for included_node in included_pipe.nodes.copy():
                unrolled_included_node = next(
                    (node for node in pipe_nodes if node["name"] == included_node["name"]), None
                )
                if unrolled_included_node:
                    doc.nodes.remove(unrolled_included_node)
    for node in doc.nodes:
        await format_node(file_parts, node, doc.includes, line_length=line_length, unroll_includes=unroll_includes)

    if not unroll_includes:
        for k, _ in doc.includes.items():
            if ".incl" not in k:
                continue
            file_parts.append(f"INCLUDE {k}")
            file_parts.append(DATAFILE_NEW_LINE)
            file_parts.append(DATAFILE_NEW_LINE)

    result = "".join(file_parts)
    result = result.rstrip("\n") + "\n"
    return result


def format_sql(sql: str, DATAFILE_INDENT: str, line_length: Optional[int] = None) -> str:
    sql = format_sql_template(sql.strip(), line_length=line_length)
    return "\n".join([f"{DATAFILE_INDENT}{part}" for part in sql.split("\n") if len(part.strip())])


async def wait_job(
    tb_client: TinyB,
    job_id: str,
    job_url: str,
    label: str,
    timeout: Optional[int] = None,
    wait_observer: Optional[Callable[[Dict[str, Any], ProgressBar], None]] = None,
    semver: Optional[str] = None,
) -> Dict[str, Any]:
    progress_bar: ProgressBar
    with click.progressbar(
        label=f"{label} ",
        length=100,
        show_eta=False,
        show_percent=wait_observer is None,
        fill_char=click.style("█", fg="green"),
    ) as progress_bar:

        def progressbar_cb(res: Dict[str, Any]):
            if wait_observer:
                wait_observer(res, progress_bar)
                return

            if "progress_percentage" in res:
                progress_bar.update(int(round(res["progress_percentage"])) - progress_bar.pos)
            elif res["status"] != "working":
                progress_bar.update(progress_bar.length if progress_bar.length else 0)

        try:
            result = await wait_job_no_ui(tb_client, job_id, timeout, progressbar_cb, semver)
            if result["status"] != "done":
                click.echo(FeedbackManager.error_while_running_job(error=result["error"]))
            return result
        except asyncio.TimeoutError:
            raise click.ClickException(FeedbackManager.error_while_running_job(error="Reach timeout, job cancelled"))
        except JobException as e:
            raise click.ClickException(FeedbackManager.error_while_running_job(error=str(e)))
        except Exception as e:
            raise click.ClickException(FeedbackManager.error_getting_job_info(error=str(e), url=job_url))


async def wait_job_no_ui(
    tb_client: TinyB,
    job_id: str,
    timeout: Optional[int] = None,
    status_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    semver: Optional[str] = None,
) -> Dict[str, Any]:
    try:
        result = await asyncio.wait_for(
            tb_client.wait_for_job(job_id, status_callback=status_callback, semver=semver), timeout
        )
        if result["status"] != "done":
            raise JobException(result.get("error"))
        return result
    except asyncio.TimeoutError:
        await tb_client.job_cancel(job_id)
        raise


async def folder_pull(
    client: TinyB,
    folder: str,
    auto: bool,
    match: Optional[str],
    prefix: Optional[str],
    force: bool,
    verbose: bool = True,
    progress_bar: bool = False,
):  # noqa: C901
    pattern = re.compile(match) if match else None

    def _get_latest_versions(resources: List[str], tag: Optional[str]):
        versions: Dict[str, Any] = {}

        for x in resources:
            t = get_name_tag_version(x, ignore_prefix=prefix is None)
            t["original_name"] = x
            if t["version"] is None:
                t["version"] = -1
            name = t["name"]

            if not tag:
                if name not in versions or name == x or versions[name]["version"] < t["version"]:
                    versions[name] = t
            elif t["tag"] == tag:
                if name in versions:
                    if versions[name]["version"] < t["version"]:
                        versions[name] = t
                else:
                    versions[name] = t

        return versions

    def get_file_folder(extension: str):
        if not auto:
            return None
        if extension == "datasource":
            return "datasources"
        if extension == "pipe":
            return "pipes"
        if extension == "token":
            return "tokens"
        return None

    async def write_files(
        versions: Dict[str, Any],
        resources: List[str],
        extension: str,
        get_resource_function: str,
        progress_bar: bool = False,
    ):
        values = versions.values()
        with click.progressbar(values, label=f"Pulling {extension}s") if progress_bar else nullcontext(values) as values:  # type: ignore
            for k in values:
                name = f"{k['name']}.{extension}"

                prefix_info = ""
                prefix_name = ""
                if not prefix:
                    if k["tag"]:
                        prefix_name = f"{k['tag']}"
                        prefix_info = f"({prefix_name})"
                else:
                    prefix_name = f"{prefix}"
                    prefix_info = f"({prefix_name})"

                try:
                    if pattern and not pattern.search(name):
                        if verbose:
                            click.echo(FeedbackManager.info_skipping_resource(resource=name))
                        continue

                    resource = await getattr(client, get_resource_function)(k["original_name"])

                    dest_folder = folder
                    if "." in k["name"] and extension != "token":
                        dest_folder = Path(folder) / "vendor" / k["name"].split(".", 1)[0]
                        name = f"{k['name'].split('.', 1)[1]}.{extension}"

                    file_folder = get_file_folder(extension)
                    f = Path(dest_folder) / file_folder if file_folder is not None else Path(dest_folder)

                    if not f.exists():
                        f.mkdir(parents=True)

                    f = f / name
                    resource_names = [x.split(".")[-1] for x in resources]

                    if verbose:
                        click.echo(FeedbackManager.info_writing_resource(resource=f, prefix=prefix_info))
                    if not f.exists() or force:
                        with open(f, "w") as fd:
                            # versions are a client only thing so
                            # datafiles from the server do not contains information about versions
                            if k["version"] >= 0:
                                resource = f"VERSION {k['version']}\n" + resource
                            if resource:
                                matches = re.findall(rf"(({prefix_name}__)?([^\s\.]*)__v\d+)", resource)
                                for match in set(matches):
                                    m = match[2].split("('")[-1]
                                    if m in resources or m in resource_names:
                                        resource = resource.replace(match[0], match[2])
                                fd.write(resource)
                    else:
                        if verbose:
                            click.echo(FeedbackManager.info_skip_already_exists())
                except Exception as e:
                    raise Exception(FeedbackManager.error_exception(error=e))
        return

    try:
        datasources = await client.datasources()
        remote_datasources = sorted([x["name"] for x in datasources])
        datasources_versions = _get_latest_versions(remote_datasources, prefix)

        pipes = await client.pipes()
        remote_pipes = sorted([x["name"] for x in pipes])
        pipes_versions = _get_latest_versions(remote_pipes, prefix)

        resources = list(datasources_versions.keys()) + list(pipes_versions.keys())

        await write_files(datasources_versions, resources, "datasource", "datasource_file", progress_bar=progress_bar)
        await write_files(pipes_versions, resources, "pipe", "pipe_file", progress_bar=progress_bar)

        return

    except Exception as e:
        raise click.ClickException(FeedbackManager.error_pull(error=str(e)))


def color_diff(diff: Iterable[str]) -> Generator[str, Any, None]:
    for line in diff:
        if line.startswith("+"):
            yield Fore.GREEN + line + Fore.RESET
        elif line.startswith("-"):
            yield Fore.RED + line + Fore.RESET
        elif line.startswith("^"):
            yield Fore.BLUE + line + Fore.RESET
        else:
            yield line


def peek(iterable):
    try:
        first = next(iterable)
    except Exception:
        return None, None
    return first, itertools.chain([first], iterable)


async def diff_command(
    filenames: Optional[List[str]],
    fmt: bool,
    client: TinyB,
    no_color: Optional[bool] = False,
    with_print: Optional[bool] = True,
    verbose: Optional[bool] = None,
    clean_up: Optional[bool] = False,
    progress_bar: bool = False,
):
    def is_shared_datasource(name):
        return "." in name

    with_explicit_filenames = filenames
    verbose = True if verbose is None else verbose

    target_dir = getcwd() + os.path.sep + ".diff_tmp"
    Path(target_dir).mkdir(parents=True, exist_ok=True)

    if filenames:
        if len(filenames) == 1:
            filenames = [filenames[0]] + get_project_filenames(filenames[0])
    else:
        filenames = get_project_filenames(".")
        if verbose:
            click.echo("Saving remote resources in .diff_tmp folder.\n")
        await folder_pull(client, target_dir, False, None, None, True, verbose=verbose, progress_bar=progress_bar)

    remote_datasources: List[Dict[str, Any]] = await client.datasources()
    remote_pipes: List[Dict[str, Any]] = await client.pipes()

    local_resources = {
        Path(file).resolve().stem: file
        for file in filenames
        if (".datasource" in file or ".pipe" in file) and ".incl" not in file
    }

    changed = {}
    for resource in remote_datasources + remote_pipes:
        properties: Dict[str, Any] = get_name_tag_version(resource["name"], ignore_prefix=True)
        name = properties.get("name", None)
        if name:
            (rfilename, file) = next(
                (
                    (rfilename, file)
                    for (rfilename, file) in local_resources.items()
                    if name == rfilename and properties.get("tag", None) is None
                ),
                ("", None),
            )
            if not file:
                if not with_explicit_filenames:
                    if with_print:
                        click.echo(f"{resource['name']} only exists remotely\n")
                    if is_shared_datasource(resource["name"]):
                        changed[resource["name"]] = "shared"
                    else:
                        changed[resource["name"]] = "remote"
                continue

            suffix = ".datasource" if ".datasource" in file else ".pipe"

            if with_explicit_filenames:
                await folder_pull(
                    client, target_dir, False, resource["name"].split("__v")[0], None, True, verbose=False
                )
            target = target_dir + os.path.sep + rfilename + suffix

            diff_lines = await diff_files(target, file, with_format=fmt, with_color=(not no_color), client=client)
            not_empty, diff_lines = peek(diff_lines)
            changed[rfilename] = not_empty
            if not_empty and with_print:
                sys.stdout.writelines(diff_lines)
                click.echo("")

    for rfilename, _ in local_resources.items():
        if rfilename not in changed:
            for resource in remote_datasources + remote_pipes:
                properties = get_name_tag_version(resource["name"], ignore_prefix=True)
                name = properties.get("name", None)
                if name and name == rfilename:
                    break

                if with_print and rfilename not in changed:
                    click.echo(f"{rfilename} only exists locally\n")
                changed[rfilename] = "local"
    if clean_up:
        shutil.rmtree(target_dir)

    return changed


async def diff_files(
    from_file: str,
    to_file: str,
    from_file_suffix: str = "[remote]",
    to_file_suffix: str = "[local]",
    with_format: bool = True,
    with_color: bool = False,
    client: Optional[TinyB] = None,
):
    def file_lines(filename):
        with open(filename) as file:
            return file.readlines()

    async def parse(filename, with_format=True, unroll_includes=False):
        extension = Path(filename).suffix
        lines = None
        if extension == ".datasource":
            lines = (
                await format_datasource(filename, unroll_includes=unroll_includes, for_diff=True, client=client)
                if with_format
                else file_lines(filename)
            )
        elif extension in [".pipe", ".incl"]:
            lines = (
                await format_pipe(filename, 100, unroll_includes=unroll_includes)
                if with_format
                else file_lines(filename)
            )
        else:
            click.echo(f"Unsupported file type: {filename}")
        if lines:
            return [f"{l}\n" for l in lines.split("\n")] if with_format else lines  # noqa: E741

    lines1 = await parse(from_file, with_format)
    lines2 = await parse(to_file, with_format, unroll_includes=True)

    if not lines1 or not lines2:
        return

    diff = difflib.unified_diff(
        lines1, lines2, fromfile=f"{Path(from_file).name} {from_file_suffix}", tofile=f"{to_file} {to_file_suffix}"
    )

    if with_color:
        diff = color_diff(diff)

    return diff


async def get_current_main_workspace(client: TinyB, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    current_workspace = await client.user_workspaces_and_branches()
    workspaces: List[Dict[str, Any]] = current_workspace.get("workspaces", [])
    current_workspace = next((workspace for workspace in workspaces if workspace["id"] == config["id"]), None)
    if current_workspace.get("is_branch"):
        current_workspace = next(
            (workspace for workspace in workspaces if workspace["id"] == current_workspace["main"]), None
        )
    return current_workspace


def is_endpoint(resource: Dict[str, Any]) -> bool:
    if resource and len(resource.get("tokens", [])) != 0 and resource.get("resource") == "pipes":
        return True
    return False


def is_endpoint_with_no_dependencies(resource: Dict[str, Any], dep_map: Dict[str, Any], to_run: Dict[str, Any]) -> bool:
    if not resource or resource.get("resource") == "datasources":
        return False

    for node in resource.get("nodes", []):
        # FIXME: https://gitlab.com/tinybird/analytics/-/issues/2391
        if node.get("params", {}).get("type", "").lower() in [
            PipeNodeTypes.MATERIALIZED,
            PipeNodeTypes.COPY,
            PipeNodeTypes.DATA_SINK,
        ]:
            return False

    for key, values in dep_map.items():
        if resource["resource_name"] in values:
            r = to_run.get(key, None)
            if not r:
                continue
            return False

    deps = dep_map.get(resource["resource_name"], None)
    for dep in deps:
        r = to_run.get(dep, None)
        if is_endpoint(r):
            return False

    return True


def get_target_materialized_data_source_name(resource):
    if not resource:
        return False

    for node in resource.get("nodes", []):
        # FIXME: https://gitlab.com/tinybird/analytics/-/issues/2391
        if node.get("params", {}).get("type", "").lower() == PipeNodeTypes.MATERIALIZED:
            return node.get("params")["datasource"].split("__v")[0]


def is_datasource(resource: Dict[str, Any]) -> bool:
    if resource and resource.get("resource") == "datasources":
        return True
    return False
