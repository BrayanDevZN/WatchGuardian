"""CLI command to scaffold a project with the public WatchGuardian package."""

import argparse
from pathlib import Path

from src.project.file import copy_watchguardian


def startproject(subparsers) -> None:
    """Register the startproject command and its arguments."""
    parser = subparsers.add_parser(
        "startproject",
        help="Copy the public WatchGuardian package into a project directory",
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=None,
        help="Destination directory (defaults to the current working directory)",
    )
    parser.add_argument(
        "--name",
        default=None,
        help="Name of the copied WatchGuardian folder (defaults to WatchGuardian)",
    )


def run_startproject(args) -> Path:
    """Copy WatchGuardian using the parsed path and name arguments."""
    return copy_watchguardian(path=args.path, name=args.name)
