from pathlib import Path
import argparse

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


def project_database_path(
    project_path: str | Path,
    path: str | Path | None = None,
) -> Path:
    """Resolve a project migration DB directory, defaulting inside its data folder."""
    project_directory = Path(project_path).expanduser().resolve()
    if path is None:
        return project_directory / "data"

    selected_path = Path(path).expanduser()
    if not selected_path.is_absolute():
        selected_path = project_directory / selected_path
    return selected_path.resolve()


async def run_migrate(args) -> None:
    if args.project is not None:
        database_path = project_database_path(args.project, args.path)
        database_path.mkdir(parents=True, exist_ok=True)

        project = await load_project(
            args.project,
            config_overrides={"path": str(database_path)},
        )
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
