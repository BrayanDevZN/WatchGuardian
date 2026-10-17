"""CLI para criar e consultar o balanceador WatchGuardian."""

import importlib
import shlex
import sys

import uvicorn

from src.logs.module import Logs
from src.service.module import Cmd, Replicator, Replicators, Settings, WatchBalance

from .project import add_project_argument, load_project


logger = Logs(loglevel="SUCCESS")


def balance(subparser) -> None:
    balance_parser = subparser.add_parser(
        "balance",
        help="Criar e consultar um balanceador",
    )
    balance_commands = balance_parser.add_subparsers(
        dest="command",
        required=True,
    )

    create_parser = balance_commands.add_parser(
        "create",
        help="Criar o balanceador a partir de um objeto Python ou projeto",
    )
    create_parser.add_argument(
        "target",
        metavar="caminho:objeto",
        nargs="?",
        help=(
            "caminho importável no formato modulo:atributo; "
            "não é necessário quando --project é informado"
        ),
    )
    add_project_argument(create_parser)
    create_parser.add_argument("--host", default="127.0.0.1")
    create_parser.add_argument("--port", type=int, default=8000)
    create_parser.add_argument(
        "--detached",
        action="store_true",
        help="Iniciar o balanceador em segundo plano",
    )

    valid_parser = balance_commands.add_parser(
        "valid",
        help="Listar as URLs das réplicas saudáveis",
    )
    valid_parser.add_argument("target", metavar="caminho:objeto", nargs="?")
    add_project_argument(valid_parser)

    logs_parser = balance_commands.add_parser(
        "logs",
        help="Buscar logs nas réplicas saudáveis",
    )
    logs_parser.add_argument("target", metavar="caminho:objeto", nargs="?")
    add_project_argument(logs_parser)
    logs_parser.add_argument("--token", default=None)
    logs_parser.add_argument(
        "--env-file",
        default=None,
        help="Arquivo .env usado para obter o token (somente neste comando)",
    )


def _load_target(target: str):
    module_path, separator, object_path = target.partition(":")
    if not separator or not module_path or not object_path:
        raise ValueError(
            "Informe o alvo no formato caminho:objeto, por exemplo "
            "'config:replicas'."
        )

    module = importlib.import_module(module_path)
    value = module
    for part in object_path.split("."):
        value = getattr(value, part)

    if callable(value) and not isinstance(value, type):
        value = value()

    if not isinstance(value, (Replicators, list)):
        raise TypeError(
            "O objeto importado precisa ser Replicators, uma lista de "
            "Replicator, ou uma função que retorne um desses valores."
        )

    if isinstance(value, list) and not all(
        isinstance(replica, Replicator) for replica in value
    ):
        raise TypeError("A lista precisa conter somente objetos Replicator.")

    return value


async def _replicas(target: str) -> list[Replicator]:
    value = _load_target(target)
    return await value.get_replicas() if isinstance(value, Replicators) else value


async def _healthy_replicas(replicas: list[Replicator]) -> list[Replicator]:
    healthy = []
    for replica in replicas:
        try:
            if await replica.valid():
                healthy.append(replica)
        except Exception as error:
            logger.warning(f"Falha ao verificar {replica.url}: {error}")
    return healthy


def _print_log(item: dict, replica_url: str) -> None:
    status = str(item.get("status", "INFO")).upper()
    text = str(item.get("log", ""))
    metadata = (
        f"replica={replica_url} | "
        f"id={item.get('id')} | "
        f"public_id={item.get('public_id')} | "
        f"created_at={item.get('created_at')} | "
        f"{text}"
    )
    method = getattr(logger, status.lower(), logger.info)
    method(metadata)


def _get_token(token: str | None, env_file: str | None) -> str:
    if token:
        return token

    settings = Settings(env_file=env_file)
    settings.add_secret("token")
    return settings.required_secrets("token")


async def run_balance(args) -> None:
    if args.command == "create" and args.detached:
        command_parts = [
            sys.executable,
            "-m",
            "src.cli.main",
            "balance",
            "create",
        ]

        if args.project is not None:
            command_parts.extend(["--project", str(args.project)])
        elif args.target is not None:
            command_parts.append(args.target)
        else:
            raise SystemExit("Provide a replica target or pass --project.")

        command_parts.extend(
            ["--host", args.host, "--port", str(args.port)]
        )
        process = Cmd.detached(" ".join(shlex.quote(part) for part in command_parts))
        url = f"http://{args.host}:{args.port}"
        logger.success(
            f"Balance started at {logger.highlighted_white(url)} "
            f"(detached, PID: {process.pid})"
        )
        return

    project = await load_project(args.project)

    if project is not None:
        if project.replicators is None:
            raise RuntimeError("The project did not initialize Replicators.")
        replicas = await project.replicators.get_replicas()
    else:
        if args.target is None:
            raise SystemExit("Provide a replica target or pass --project.")
        try:
            replicas = await _replicas(args.target)
        except (ImportError, AttributeError, TypeError, ValueError) as error:
            raise SystemExit(
                f"Não foi possível carregar as réplicas: {error}"
            ) from error

    if args.command == "create":
        app = (
            project.balance_app
            if project is not None
            else WatchBalance(replicas=replicas).run()
        )
        url = f"http://{args.host}:{args.port}"
        logger.success(f"Balance started at {logger.highlighted_white(url)}")
        config = uvicorn.Config(
            app,
            host=args.host,
            port=args.port,
            log_config=None,
            log_level="critical",
            access_log=False,
        )
        server = uvicorn.Server(config)
        await server.serve()
        return

    healthy = await _healthy_replicas(replicas)

    if args.command == "valid":
        if not healthy:
            logger.warning("Nenhuma réplica saudável encontrada.")
            return

        for replica in healthy:
            logger.success(replica.url)
        return

    if args.command == "logs":
        try:
            if project is not None:
                token = (
                    args.token
                    if args.token is not None
                    else project.settings.required_secrets("token")
                )
            else:
                token = _get_token(args.token, args.env_file)
        except Exception as error:
            raise SystemExit(f"Não foi possível obter o token: {error}") from error

        if not healthy:
            logger.warning("Nenhuma réplica saudável encontrada.")
            return

        for replica in healthy:
            records = await replica.logs(token=token).get_log()
            if records is None:
                continue
            if isinstance(records, dict):
                records = [records]
            for record in records:
                _print_log(record, replica.url)
