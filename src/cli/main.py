"""
Junta todos os comandos CLI
"""

from .migrate import migrate, run_migrate
from .auth import auth, run_auth
from .server import server, run_server

import argparse
import asyncio


async def run() -> None:

    parser = argparse.ArgumentParser()

    modules = parser.add_subparsers(
        dest="module",
        required=True
    )

    commands = [
        migrate,
        auth,
        server,
    ]

    for command in commands:
        command(modules)

    args = parser.parse_args()

    if args.module == "migrate":
        await run_migrate(args)

    elif args.module == "auth":
        await run_auth(args)

    elif args.module == "server":
        await run_server(args)


def main() -> None:
    asyncio.run(run())

main()
