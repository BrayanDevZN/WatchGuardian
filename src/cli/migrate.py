from src.service.db import WatchDb, Settings
import argparse


def migrate(subparser) -> None:

    migrate_parser = subparser.add_parser("migrate")

    migrate_parser.add_argument("--env-file")

    migrate_cmd = migrate_parser.add_subparsers(
        dest="command",
        required=True
    )

    migrate_cmd.add_parser("make_tables")
    migrate_cmd.add_parser("reset")
    migrate_cmd.add_parser("drop")


async def run_migrate(args) -> None:

    env = args.env_file

    settings = (
        Settings(env_file=env)
        if env is not None
        else Settings()
    )

    control_db = await WatchDb(
        settings=settings
    )

    if args.command == "make_tables":
        await control_db.create_tables()

    elif args.command == "reset":
        await control_db.reset_tables()

    elif args.command == "drop":
        await control_db.drop_tables()

    



    
    