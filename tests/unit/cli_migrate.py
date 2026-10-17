"""Tests migration database paths and the --project/--path options."""

import argparse
import asyncio
import importlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

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


def test_project_migration_does_not_start_all_modules() -> None:
    migrate_cli = importlib.import_module("src.cli.migrate")
    events = []

    class FakeApp:
        http = None

        async def load_module(self):
            raise AssertionError("migrate must not load server and balance modules")

    class FakeDatabase:
        def __init__(self, *, settings, http):
            events.append(("database_init", settings, http))

        def __await__(self):
            async def ready():
                events.append(("database_ready",))
                return self

            return ready().__await__()

        async def create_tables(self):
            events.append(("create_tables",))

    with TemporaryDirectory() as temporary_directory:
        project = Path(temporary_directory)
        _project_settings(project)
        args = argparse.Namespace(
            project=project,
            path=None,
            env_file=None,
            command="make_tables",
        )

        with (
            patch.object(migrate_cli, "load_project_app", return_value=FakeApp()),
            patch.object(migrate_cli, "load_project_settings", return_value="settings"),
            patch.object(migrate_cli, "WatchDb", FakeDatabase),
        ):
            asyncio.run(migrate_cli.run_migrate(args))

    assert [event[0] for event in events] == [
        "database_init",
        "database_ready",
        "create_tables",
    ]


if __name__ == "__main__":
    test_project_and_path_before_migrate_action()
    test_project_and_path_after_migrate_action()
    test_project_migration_does_not_start_all_modules()
    print("Migrate CLI project path tests passed")
