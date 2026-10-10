"""
Junta todos os comandos CLI
"""

from .migrate import migrate, run_migrate

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
    ]

    for command in commands:
        command(modules)

    args = parser.parse_args()

    if args.module == "migrate":
        await run_migrate(args)


def main() -> None:
    asyncio.run(run())

main()