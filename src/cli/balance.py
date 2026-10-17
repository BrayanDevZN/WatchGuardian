"""CLI para criar e executar o balanceador WatchGuardian."""

import argparse
import importlib
from collections.abc import Callable

import uvicorn

from src.logs.module import Logs
from src.replicator.module import Replicator, Replicators
from src.service.balance import WatchBalance


logger = Logs(loglevel="SUCCESS")


def balance(subparser) -> None:
    balance_parser = subparser.add_parser(
        "balance",
        help="Criar e executar um balanceador",
    )
    balance_commands = balance_parser.add_subparsers(
        dest="command",
        required=True,
    )

    create_parser = balance_commands.add_parser(
        "create",
        help="Criar o balanceador a partir de um objeto Python",
    )
    create_parser.add_argument(
        "target",
        metavar="caminho:objeto",
        help=(
            "caminho importável no formato modulo:atributo; "
            "o atributo deve ser Replicators, uma lista de Replicator "
            "ou uma função que retorne um desses valores"
        ),
    )
    create_parser.add_argument("--host", default="127.0.0.1")
    create_parser.add_argument("--port", type=int, default=8000)


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


async def run_balance(args) -> None:
    if args.command != "create":
        return

    try:
        replicas = _load_target(args.target)
    except (ImportError, AttributeError, TypeError, ValueError) as error:
        raise SystemExit(f"Não foi possível carregar o balanceador: {error}") from error

    app = WatchBalance(replicas=replicas).run()
    logger.success(f"Balance iniciado em http://{args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port)
