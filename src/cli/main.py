"""junta todos os comandos cli"""

from .migrate import migrate
import argparse 
import asyncio

async def main() -> None:

    commands = [
        migrate
    ]

    parser = argparse.ArgumentParser()

    for command in commands:

        await command(subparser=parser)



asyncio.run(main())