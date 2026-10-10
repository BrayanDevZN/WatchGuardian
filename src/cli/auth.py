"""
Comandos CLI de autenticação.
"""

import argparse
import json

from src.logs.module import Logs
from src.service.module import Settings, WatchAuth


logger = Logs(loglevel="SUCCESS")


def auth(subparser) -> None:

    auth_parser = subparser.add_parser("auth")

    auth_parser.add_argument("--env-file")

    auth_cmd = auth_parser.add_subparsers(
        dest="command",
        required=True
    )

    auth_cmd.add_parser("secret")

    token_parser = auth_cmd.add_parser("token")
    token_parser.add_argument(
        "--payload",
        default="{}"
    )


async def run_auth(args) -> None:

    if args.command == "secret":
        watch_auth = WatchAuth()
        secret = watch_auth.secret()

        logger.success(
            f"Secret: {secret}"
        )

    elif args.command == "token":
        env = args.env_file

        settings = (
            Settings(env_file=env)
            if env is not None
            else Settings()
        )

        settings.add_secret("secret")
        settings.required_secrets("secret")

        watch_auth = WatchAuth(
            settings=settings
        )

        payload = json.loads(
            args.payload
        )

        token = await watch_auth.encode(
            payload=payload
        )

        logger.success(
            f"Token: {token}"
        )
