import argparse
import json
import os
from pathlib import Path

from src.project.watchguardian.settings import (
    DEFAULT_CONFIGS,
    ProjectSettings,
    resolve_project_configs,
)
from src.service.module import Settings, WatchDb
from .project import (
    add_project_argument,
    load_project_app,
    load_project_settings,
    resolve_project_path,
)


def migrate(subparser) -> None:
    migrate_parser = subparser.add_parser("migrate")
    migrate_parser.add_argument("--env-file")
    add_project_argument(migrate_parser)
    migrate_parser.add_argument(
        "--path",
        type=Path,
        default=None,
        help="SQLite directory (project-relative with --project)",
    )

    migrate_cmd = migrate_parser.add_subparsers(dest="command", required=True)
    for command in ("make_tables", "reset", "drop"):
        command_parser = migrate_cmd.add_parser(command)
        add_project_argument(command_parser, default=argparse.SUPPRESS)
        command_parser.add_argument(
            "--path",
            type=Path,
            default=argparse.SUPPRESS,
            help="SQLite directory (project-relative with --project)",
        )


def configure_project_database_path(
    project_path: str | Path,
    path: str | Path | None = None,
) -> Path:
    """Persist and create the project's SQLite directory."""
    project_directory = Path(project_path).expanduser().resolve()
    settings_path = project_directory / "settings.json"
    if not settings_path.is_file():
        raise FileNotFoundError(f"Project settings file was not found: {settings_path}")

    with settings_path.open(encoding="utf-8") as settings_file:
        project_settings = json.load(settings_file)

    requested_path = Path(path).expanduser() if path is not None else Path("data")
    if requested_path.is_absolute():
        database_directory = requested_path.resolve()
        stored_path = str(database_directory)
    else:
        database_directory = (project_directory / requested_path).resolve()
        stored_path = requested_path.as_posix()

    database_directory.mkdir(parents=True, exist_ok=True)
    project_settings.setdefault("configs", {})["path"] = stored_path
    settings_path.write_text(
        json.dumps(project_settings, indent=4) + "\n", encoding="utf-8"
    )
    return database_directory


def _load_environment_settings(env_file: str | None, path: Path | None) -> Settings:
    env_path = Path(env_file).expanduser() if env_file is not None else Path.cwd() / ".env"
    environment_present = env_path.is_file() or any(
        os.getenv(name)
        for name in ("url_db", "URL_DB", "DATABASE_URL", "host", "HOST")
    )
    if not environment_present:
        raise RuntimeError(
            "No WatchGuardian project was found and no .env file or database "
            "environment variables are configured. Create ./watchguardian or pass --env-file."
        )

    settings = ProjectSettings(
        env_file=str(env_path.resolve()) if env_path.is_file() else None,
        local=True,
    ).get()
    configs = resolve_project_configs(Path.cwd(), DEFAULT_CONFIGS)
    for name, value in configs.items():
        settings.add_config({"name": name, "value": value})

    if path is not None:
        database_path = path.expanduser().resolve()
        database_path.mkdir(parents=True, exist_ok=True)
        settings.add_config({"name": "path", "value": str(database_path)})
    return settings


async def run_migrate(args) -> None:
    project_path = resolve_project_path(args.project)
    if project_path is not None:
        configure_project_database_path(project_path, args.path)
        project_app = load_project_app(project_path)
        settings = load_project_settings(project_app)
        # Migrations must not boot WatchLogs, WatchServer, or WatchBalance.
        control_db = await WatchDb(settings=settings, http=project_app.http)
    else:
        settings = _load_environment_settings(args.env_file, args.path)
        control_db = await WatchDb(settings=settings)

    if args.command == "make_tables":
        await control_db.create_tables()
    elif args.command == "reset":
        await control_db.reset_tables()
    elif args.command == "drop":
        await control_db.drop_tables()
