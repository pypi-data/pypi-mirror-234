import argparse
import json
import logging as pylogging
import os
import sys
import traceback
from pathlib import Path
from typing import List, Optional

from pydantic import ValidationError

from chalk.config.project_config import load_project_config
from chalk.importer import import_all_files
from chalk.parsed.user_types_to_json import get_registered_types_as_json
from chalk.utils.stubgen import configure_stubgen_argparse, run_stubgen


def _get_list_results(directory: Optional[str], file_allowlist: Optional[List[str]]):
    scope_to = Path(directory or os.getcwd())
    try:
        failed = import_all_files(file_allowlist=file_allowlist)
        return get_registered_types_as_json(scope_to, failed)
    except Exception:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        assert ex_type is not None
        relevant_traceback = f"""{os.linesep.join(traceback.format_tb(ex_traceback))}
\n{ex_type.__name__}: {str(ex_value)}
"""
        return json.dumps(dict(failed=[dict(traceback=relevant_traceback)]), indent=2)


def dump_cmd(filename: str, directory: Optional[str], filter_file: Optional[str]):
    file_allowlist = None
    if filter_file is not None and os.path.exists(filter_file):
        with open(filter_file) as f:
            file_allowlist = [f.strip() for f in f.readlines()]

    with open(filename, "w") as f:
        f.write(
            _get_list_results(
                directory=directory,
                file_allowlist=file_allowlist,
            )
        )


def list_cmd(directory: str):
    print(_get_list_results(directory=directory, file_allowlist=None))


def config_cmd():
    json_response: str
    try:
        model = load_project_config()
    except ValidationError as e:
        json_response = json.dumps({"error": str(e)})
    else:
        if model is None:
            print("No `chalk.yaml` configuration file found")
            return
        json_response = model.json()

    print(json_response)


def cli(args_override: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        prog="Chalk Python CLI",
        description=(
            "You typically do not need to invoke this utility directly. "
            "Prefer https://github.com/chalk-ai/cli instead."
        ),
    )
    parser.add_argument("--log-level", help="Print debug info", nargs="?")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("config", help="Print the config for the current project")
    list_parser = subparsers.add_parser("list", help="List the resolvers for the current project and print as json")
    list_parser.add_argument("--directory", help="Scope to this directory", nargs="?")
    dump_parser = subparsers.add_parser("dump", help="Write the resolvers for the current project to the given file")
    dump_parser.add_argument("filename", help="Write to this file")
    dump_parser.add_argument("--directory", help="Scope to this directory", nargs="?")
    export_parser = subparsers.add_parser(
        "export", help="Write the resolvers for the current project to the given file"
    )
    export_parser.add_argument("filename", help="Write to this file")
    export_parser.add_argument("--directory", help="Scope to this directory", nargs="?")
    export_parser.add_argument("--file_filter", help="Path containing only files to consider", nargs="?")
    stubgen_parser = subparsers.add_parser("stubgen", help="Generate type stubs for feature set classes")
    stubgen_parser.add_argument("--file_filter", help="Path containing only files to consider", nargs="?")
    configure_stubgen_argparse(stubgen_parser)

    # Parsing only known args for forwards compatibility.
    # Changing this to `.parse_args` means once the args are
    # set for a command, you can never add to them.
    # Please do not change to `.parse_args`.
    args, _ = parser.parse_known_args(args_override)
    if args.log_level:
        level = getattr(pylogging, args.log_level.upper())
        pylogging.basicConfig(
            format="%(asctime)s %(levelname)s: %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
            level=level,
        )

    if args.command == "list":
        list_cmd(args.directory)

    elif args.command == "config":
        config_cmd()

    elif args.command == "stubgen":
        run_stubgen(args, args.file_filter)

    elif args.command == "export":
        dump_cmd(args.filename, args.directory, args.file_filter)

    elif args.command == "dump":
        dump_cmd(args.filename, args.directory, None)

    else:
        parser.print_help(sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(cli())
