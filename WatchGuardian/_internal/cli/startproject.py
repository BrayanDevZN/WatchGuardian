"""CLI command to scaffold a project with the public WatchGuardian package."""

import argparse
from pathlib import Path

from WatchGuardian._internal.project.file import copy_watchguardian


def _add_arguments(parser: argparse.ArgumentParser) -> None:
    """Register startproject command arguments on a parser."""
    parser.add_argument(
        "--path",
        type=Path,
        default=None,
        help="Destination directory (defaults to the current working directory)",
    )
    parser.add_argument(
        "--name",
        default=None,
        help="Lowercase project package name (defaults to watchguardian; that name cannot be passed explicitly)",
    )
    parser.add_argument(
        "--env-file",
        default=None,
        help="Environment file used by the generated project (defaults to local settings)",
    )


def startproject(subparsers) -> None:
    """Register the startproject subcommand."""
    parser = subparsers.add_parser(
        "startproject",
        help="Copy the public WatchGuardian package into a project directory",
    )
    _add_arguments(parser)


def run_startproject(args) -> Path:
    """Copy WatchGuardian and generate the project configuration."""
    return copy_watchguardian(
        path=args.path,
        name=args.name,
        env_file=args.env_file,
    )


def main() -> None:
    """Run the standalone watchguardian-startproject command."""
    parser = argparse.ArgumentParser(
        prog="watchguardian-startproject",
        description="Create a project from the WatchGuardian template",
    )
    _add_arguments(parser)
    args = parser.parse_args()
    run_startproject(args)
