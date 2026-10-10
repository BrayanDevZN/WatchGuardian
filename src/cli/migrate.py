from src.service.db import WatchDb, Settings
import argparse

async def migrate(subparser:argparse.ArgumentParser):

    subparser.add_argument("--env-file")

    module = subparser.add_subparsers(dest="migrate")

    migrate = module.add_parser("migrate")

    migrate_cmd = migrate.add_subparsers(dest="command")

    migrate_cmd.add_parser("make_tables")
    migrate_cmd.add_parser("reset")
    migrate_cmd.add_parser("drop")

    args = subparser.parse_args()

    env = args.env_file

    settings = Settings(env_file=env) if env is not None else Settings()

    command = args.command

    control_db = await WatchDb(settings=settings)
    

    if command == "make_tables":

        await control_db.create_tables()

    elif command == "reset":

        await control_db.reset_tables()

    elif command == "drop":


        await control_db.drop_tables()

   
    




    

    



    
    