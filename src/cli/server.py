"""Comandos CLI para executar e consultar o servidor."""

import argparse

from src.logs.module import Logs
from src.service.module import ClientHttp, Cmd, Settings


logger = Logs(loglevel="SUCCESS")


def server(subparser) -> None:
    server_parser = subparser.add_parser("server")
    server_parser.add_argument("--env-file")

    server_cmd = server_parser.add_subparsers(
        dest="command",
        required=True,
    )

    run_parser = server_cmd.add_parser("run")
    run_parser.add_argument("module")
    run_parser.add_argument("--host", default="127.0.0.1")
    run_parser.add_argument("--port", type=int, default=8000)
    run_parser.add_argument("--detached", action="store_true")

    logs_parser = server_cmd.add_parser("logs")
    logs_parser.add_argument("--token", default=None)

    obs_parser = server_cmd.add_parser("obs")
    obs_parser.add_argument("--token", default=None)


def _settings(env_file: str | None) -> Settings:
    return (
        Settings(env_file=env_file)
        if env_file is not None
        else Settings()
    )


def _token(settings: Settings, token: str | None) -> str:
    if token is not None:
        return token

    settings.add_secret("token")
    return settings.required_secrets("token")


def _print_log(item: dict) -> None:
    status = str(item.get("status", "INFO")).upper()
    text = str(item.get("log", ""))

    metadata = (
        f"id={item.get('id')} | "
        f"public_id={item.get('public_id')} | "
        f"created_at={item.get('created_at')} | "
        f"{text}"
    )

    method = getattr(logger, status.lower(), logger.info)
    method(metadata)


def _print_obs(item: dict) -> None:
    status = str(item.get("status", "pending")).lower()

    methods = {
        "sucess": logger.success,
        "pending": logger.info,
        "failure": logger.error,
    }

    text = (
        f"id={item.get('id')} | "
        f"public_id={item.get('public_id')} | "
        f"task={item.get('task')} | "
        f"latency={item.get('latency')} | "
        f"content={item.get('content')} | "
        f"created_at={item.get('created_at')}"
    )

    methods.get(status, logger.info)(text)


async def run_server(args) -> None:
    settings = _settings(args.env_file)

    if args.command == "run":
        command = (
            f"uvicorn {args.module} "
            f"--host {args.host} "
            f"--port {args.port}"
        )

        if args.detached:
            process = Cmd.detached(command)
            logger.success(
                f"Servidor iniciado em detached. PID: {process.pid}"
            )
            return

        Cmd.run(command)
        return

    token = _token(
        settings=settings,
        token=args.token,
    )

    client = ClientHttp(settings=settings)

    if args.command == "logs":
        data = await client.logs(token=token).get_log()

        if data is None:
            return

        for item in data:
            _print_log(item)

    elif args.command == "obs":
        data = await client.obs(token=token).get_obs()

        if data is None:
            return

        for item in data:
            _print_obs(item)
