"""Tests project-relative migration paths and CLI option placement."""

import argparse
from pathlib import Path

from src.cli.migrate import migrate, project_database_path


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    modules = parser.add_subparsers(dest="module", required=True)
    migrate(modules)
    return parser


def test_project_option_and_path_before_migrate_action() -> None:
    args = _parser().parse_args(
        ["migrate", "--project", "WatchGuardian", "--path", "custom", "make_tables"]
    )
    assert args.command == "make_tables"
    assert args.project == Path("WatchGuardian")
    assert args.path == Path("custom")


def test_project_option_and_path_after_migrate_action() -> None:
    args = _parser().parse_args(
        ["migrate", "make_tables", "--project", "WatchGuardian", "--path", "custom"]
    )
    assert args.command == "make_tables"
    assert args.project == Path("WatchGuardian")
    assert args.path == Path("custom")


def test_project_database_defaults_to_project_data_directory(tmp_path: Path) -> None:
    assert project_database_path(tmp_path) == (tmp_path / "data").resolve()


def test_relative_database_override_is_inside_project(tmp_path: Path) -> None:
    assert project_database_path(tmp_path, "custom-data") == (
        tmp_path / "custom-data"
    ).resolve()


def test_absolute_database_override_is_preserved(tmp_path: Path) -> None:
    external_path = tmp_path.parent / "external-data"
    assert project_database_path(tmp_path, external_path) == external_path.resolve()


if __name__ == "__main__":
    test_project_option_and_path_before_migrate_action()
    test_project_option_and_path_after_migrate_action()
    test_project_database_defaults_to_project_data_directory(Path.cwd())
    test_relative_database_override_is_inside_project(Path.cwd())
    print("Migrate CLI project path tests passed")
