import argparse
import json
from pathlib import Path

from src.service.module import Settings, WatchDb
from .project import add_project_argument, load_project


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

    migrate_cmd = migrate_parser.add_subparsers(
        dest="command",
        required=True
    )

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
        json.dumps(project_settings, indent=4) + "\n",
        encoding="utf-8",
    )
    return database_directory


async def run_migrate(args) -> None:
    if args.project is not None:
        configure_project_database_path(args.project, args.path)
        project = await load_project(args.project)
        control_db = project.watch_db
    else:
        env = args.env_file
        settings = Settings(env_file=env) if env is not None else Settings()

        if args.path is not None:
            database_path = Path(args.path).expanduser().resolve()
            database_path.mkdir(parents=True, exist_ok=True)
            settings.add_config({"name": "path", "value": str(database_path)})

        control_db = await WatchDb(settings=settings)

    if args.command == "make_tables":
        await control_db.create_tables()
    elif args.command == "reset":
        await control_db.reset_tables()
    elif args.command == "drop":
        await control_db.drop_tables()
