"""Tests accepted placements of the migrate --project option."""

import argparse

from src.cli.migrate import migrate


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    modules = parser.add_subparsers(dest="module", required=True)
    migrate(modules)
    return parser


def test_project_option_before_migrate_action() -> None:
    args = _parser().parse_args(
        ["migrate", "--project", "WatchGuardian", "make_tables"]
    )
    assert args.command == "make_tables"
    assert args.project.name == "WatchGuardian"


def test_project_option_after_migrate_action() -> None:
    args = _parser().parse_args(
        ["migrate", "make_tables", "--project", "WatchGuardian"]
    )
    assert args.command == "make_tables"
    assert args.project.name == "WatchGuardian"


if __name__ == "__main__":
    test_project_option_before_migrate_action()
    test_project_option_after_migrate_action()
    print("Migrate CLI project argument tests passed")
