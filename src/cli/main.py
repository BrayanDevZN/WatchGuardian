"""
Junta todos os comandos CLI
"""

from .migrate import migrate, run_migrate
from .auth import auth, run_auth

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
    ]

    for command in commands:
        command(modules)

    args = parser.parse_args()

    if args.module == "migrate":
        await run_migrate(args)

    elif args.module == "auth":
        await run_auth(args)


def main() -> None:
    asyncio.run(run())

main()