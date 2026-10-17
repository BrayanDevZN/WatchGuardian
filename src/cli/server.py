"""Comandos CLI para executar e consultar o servidor."""

import argparse
import shlex
import sys

import uvicorn

from src.logs.module import Logs
from src.service.module import ClientHttp, Cmd, Settings, WatchDb

from .migrate import run_migrate
from .project import add_project_argument, load_project_modules, resolve_project_path


logger = Logs(loglevel="SUCCESS")


def server(subparser) -> None:
    server_parser = subparser.add_parser("server")
    server_parser.add_argument("--env-file")

    server_cmd = server_parser.add_subparsers(
        dest="command",
        required=True,
    )

    run_parser = server_cmd.add_parser("run")
    run_parser.add_argument("app", nargs="?")
    add_project_argument(run_parser)
    run_parser.add_argument("--host", default="127.0.0.1")
    run_parser.add_argument("--port", type=int, default=8000)
    run_parser.add_argument("--detached", action="store_true")

    logs_parser = server_cmd.add_parser("logs")
    add_project_argument(logs_parser)
    logs_parser.add_argument("--token", default=None)
    logs_parser.add_argument(
        "--realtime",
        action="store_true",
        default=False,
        help="Stream new logs through the WebSocket instead of fetching over HTTP",
    )

    obs_parser = server_cmd.add_parser("obs")
    add_project_argument(obs_parser)
    obs_parser.add_argument("--token", default=None)
    obs_parser.add_argument(
        "--realtime",
        action="store_true",
        default=False,
        help="Stream new observability events through the WebSocket instead of fetching over HTTP",
    )


def _settings(env_file: str | None) -> Settings:
    return Settings(env_file=env_file) if env_file is not None else Settings()


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
        f"memory_bytes={item.get('memory_bytes')} | "
        f"content={item.get('content')} | "
        f"created_at={item.get('created_at')}"
    )

    methods.get(status, logger.info)(text)


async def run_server(args) -> None:
    if args.command == "run" and args.detached and resolve_project_path(args.project) is not None:
        project_path = resolve_project_path(args.project)
        command_parts = [
            sys.executable,
            "-m",
            "src.cli.main",
            "server",
            "run",
            "--project",
            str(project_path),
            "--host",
            args.host,
            "--port",
            str(args.port),
        ]
        process = Cmd.detached(" ".join(shlex.quote(part) for part in command_parts))
        url = f"http://{args.host}:{args.port}"
        logger.success(
            f"Project server started at {logger.highlighted_white(url)} "
            f"(detached, PID: {process.pid})"
        )
        return

    requested_modules = ("server",) if args.command == "run" else ("client",)
    project = await load_project_modules(args.project, requested_modules)

    if args.command == "run":
        if project is not None:
            if not args.detached and not project.http:
                database = await WatchDb(
                    settings=project.settings,
                    http=project.http,
                )
                await database.create_tables()

            app = project.server_app
            url = f"http://{args.host}:{args.port}"
            logger.success(f"Server started at {logger.highlighted_white(url)}")
            config = uvicorn.Config(
                app,
                host=args.host,
                port=args.port,
                log_config=None,
                log_level="critical",
                access_log=False,
            )
            await uvicorn.Server(config).serve()
            return

        if args.app is None:
            raise SystemExit("Provide an ASGI app target or pass --project.")

        migrate_args = argparse.Namespace(
            env_file=args.env_file,
            project=None,
            command="make_tables",
            path=None,
        )
        await run_migrate(migrate_args)

        command = (
            f"uvicorn {args.app} "
            f"--host {args.host} "
            f"--port {args.port} "
            "--log-level critical "
            "--no-access-log"
        )
        url = f"http://{args.host}:{args.port}"

        if args.detached:
            process = Cmd.detached(command)
            logger.success(
                f"Server started at {logger.highlighted_white(url)} "
                f"(detached, PID: {process.pid})"
            )
            return

        logger.success(f"Server started at {logger.highlighted_white(url)}")
        Cmd.run(command)
        return

    if project is not None:
        token = (
            args.token
            if args.token is not None
            else project.settings.required_secrets("token")
        )
        client = project.client_http
    else:
        settings = _settings(args.env_file)
        token = _token(settings=settings, token=args.token)
        client = ClientHttp(settings=settings)

    if args.command == "logs":
        if args.realtime:
            async for event in client.listen_logs(token=token):
                _print_log(event["data"])
            return

        data = await client.logs(token=token).get_log()

        if data is None:
            return

        for item in data:
            _print_log(item)

    elif args.command == "obs":
        if args.realtime:
            async for event in client.listen_obs(token=token):
                _print_obs(event["data"])
            return

        data = await client.obs(token=token).get_obs()

        if data is None:
            return

        for item in data:
            _print_obs(item)
