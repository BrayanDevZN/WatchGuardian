from src.service.module import Settings, WatchDb
from .project import add_project_argument, load_project
import argparse


def migrate(subparser) -> None:
    migrate_parser = subparser.add_parser("migrate")
    migrate_parser.add_argument("--env-file")
    add_project_argument(migrate_parser)

    migrate_cmd = migrate_parser.add_subparsers(
        dest="command",
        required=True
    )

    for command in ("make_tables", "reset", "drop"):
        command_parser = migrate_cmd.add_parser(command)
        add_project_argument(command_parser, default=argparse.SUPPRESS)


async def run_migrate(args) -> None:
    project = await load_project(args.project)

    if project is not None:
        control_db = project.watch_db
    else:
        env = args.env_file
        settings = Settings(env_file=env) if env is not None else Settings()
        control_db = await WatchDb(settings=settings)

    if args.command == "make_tables":
        await control_db.create_tables()
    elif args.command == "reset":
        await control_db.reset_tables()
    elif args.command == "drop":
        await control_db.drop_tables()
