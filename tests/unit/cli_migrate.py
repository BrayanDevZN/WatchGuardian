"""Tests migration database paths and the --project/--path options."""

import argparse
import json
from pathlib import Path

from src.cli.migrate import configure_project_database_path, migrate
from src.project.watchguardian.settings import resolve_project_configs


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    modules = parser.add_subparsers(dest="module", required=True)
    migrate(modules)
    return parser


def _project_settings(project: Path) -> Path:
    project.mkdir(parents=True, exist_ok=True)
    settings_path = project / "settings.json"
    settings_path.write_text(
        json.dumps({"name": project.name, "configs": {"path": None}}),
        encoding="utf-8",
    )
    return settings_path


def test_project_and_path_before_migrate_action() -> None:
    args = _parser().parse_args(
        ["migrate", "--project", "WatchGuardian", "--path", "custom", "make_tables"]
    )
    assert args.command == "make_tables"
    assert args.project == Path("WatchGuardian")
    assert args.path == Path("custom")


def test_project_and_path_after_migrate_action() -> None:
    args = _parser().parse_args(
        ["migrate", "make_tables", "--project", "WatchGuardian", "--path", "custom"]
    )
    assert args.command == "make_tables"
    assert args.project == Path("WatchGuardian")
    assert args.path == Path("custom")


def test_migration_default_persists_data_directory_inside_project(
    tmp_path: Path,
) -> None:
    settings_path = _project_settings(tmp_path)
    database_directory = configure_project_database_path(tmp_path)

    assert database_directory == (tmp_path / "data").resolve()
    assert database_directory.is_dir()
    assert json.loads(settings_path.read_text())["configs"]["path"] == "data"


def test_custom_relative_path_is_persisted_and_project_relative(
    tmp_path: Path,
) -> None:
    settings_path = _project_settings(tmp_path)
    database_directory = configure_project_database_path(tmp_path, "custom-data")

    assert database_directory == (tmp_path / "custom-data").resolve()
    assert database_directory.is_dir()
    assert json.loads(settings_path.read_text())["configs"]["path"] == "custom-data"


def test_app_resolves_database_path_from_project_root(tmp_path: Path) -> None:
    configs = resolve_project_configs(tmp_path, {"path": "data"})

    assert configs["path"] == str((tmp_path / "data").resolve())
    assert (tmp_path / "data").is_dir()


if __name__ == "__main__":
    test_project_and_path_before_migrate_action()
    test_project_and_path_after_migrate_action()
    print("Migrate CLI project path tests passed")
