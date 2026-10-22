"""Manage generated WatchGuardian projects from the CLI."""

import argparse
import json
import shutil
from pathlib import Path
from secrets import token_urlsafe

from dotenv import dotenv_values

from src.logs.module import Logs
from src.project.file import copy_watchguardian
from src.project.watchguardian.settings import DEFAULT_CONFIGS

logger = Logs(loglevel="SUCCESS")

LOCAL_SECRETS = {
    "host": "localhost",
    "port": "6379",
    "password": "",
    "origin": "*",
    "rate_limit": "100",
    "secret": None,
    "url": "http://localhost:8000",
    "token": "",
    "url_db": "",
}


def _project_path(value: str | Path | None) -> Path:
    path = Path(value).expanduser() if value is not None else Path.cwd() / "watchguardian"
    path = path.resolve()
    if not path.is_dir():
        raise FileNotFoundError(f"Project directory does not exist: {path}")
    if not (path / "main.py").is_file() or not (path / "settings.json").is_file():
        raise ValueError(f"Not a WatchGuardian project directory: {path}")
    return path


def _write_env(path: Path, source: str | Path | None = None) -> None:
    values = dict(LOCAL_SECRETS)
    values["secret"] = token_urlsafe(32)
    values.update(DEFAULT_CONFIGS)

    if source is not None:
        source_path = Path(source).expanduser().resolve()
        if not source_path.is_file():
            raise FileNotFoundError(f"Environment file does not exist: {source_path}")
        for name, value in dotenv_values(source_path).items():
            if value is not None:
                values[name] = value

    lines = ["# WatchGuardian local environment"]
    for name, value in values.items():
        rendered = json.dumps(value) if isinstance(value, (list, dict)) else value
        lines.append(f"{name}={rendered}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def project(subparsers) -> None:
    parser = subparsers.add_parser("project", help="Create and manage a project")
    commands = parser.add_subparsers(dest="project_command", required=True)

    start_parser = commands.add_parser("start", help="Create a WatchGuardian project")
    start_parser.add_argument("--path", type=Path, default=None)
    start_parser.add_argument("--name", default=None)
    start_parser.add_argument("--env-file", type=Path, default=None)
    start_parser.add_argument(
        "--with_env",
        "--with-env",
        dest="with_env",
        action="store_true",
        help="Create a .env file populated with local defaults",
    )

    reset_parser = commands.add_parser(
        "reset", help="Reset project settings and .env to local defaults"
    )
    reset_parser.add_argument("--project", type=Path, default=None)

    delete_parser = commands.add_parser("delete", help="Delete a generated project")
    delete_parser.add_argument("--project", type=Path, default=None)


def run_project(args) -> Path | None:
    if args.project_command == "start":
        source_env = args.env_file.expanduser().resolve() if args.env_file else None
        if source_env is not None and not source_env.is_file():
            raise FileNotFoundError(f"Environment file does not exist: {source_env}")

        destination = copy_watchguardian(
            path=args.path,
            name=args.name,
            env_file=None if args.with_env else source_env,
        )
        if args.with_env:
            _write_env(destination / ".env", source_env)
            settings_path = destination / "settings.json"
            config = json.loads(settings_path.read_text(encoding="utf-8"))
            config.update(env_file=".env", local=True, http=None)
            settings_path.write_text(
                json.dumps(config, indent=4) + "\n", encoding="utf-8"
            )
        return destination

    directory = _project_path(args.project)
    settings_path = directory / "settings.json"
    config = json.loads(settings_path.read_text(encoding="utf-8"))

    if args.project_command == "reset":
        _write_env(directory / ".env")
        config.update(
            env_file=".env",
            local=True,
            http=None,
            configs=dict(DEFAULT_CONFIGS),
        )
        settings_path.write_text(
            json.dumps(config, indent=4) + "\n", encoding="utf-8"
        )
        logger.success(f"Project reset to local defaults at '{directory}'.")
        return directory

    if args.project_command == "delete":
        shutil.rmtree(directory)
        logger.success(f"Project deleted at '{directory}'.")
        return None

    raise ValueError(f"Unknown project command: {args.project_command}")


def main() -> None:
    """Standalone project management entry point."""
    parser = argparse.ArgumentParser(prog="watchguardian project")
    commands = parser.add_subparsers(dest="project_command", required=True)
    start_parser = commands.add_parser("start")
    start_parser.add_argument("--path", type=Path, default=None)
    start_parser.add_argument("--name", default=None)
    start_parser.add_argument("--env-file", type=Path, default=None)
    start_parser.add_argument("--with_env", "--with-env", dest="with_env", action="store_true")
    reset_parser = commands.add_parser("reset")
    reset_parser.add_argument("--project", type=Path, default=None)
    delete_parser = commands.add_parser("delete")
    delete_parser.add_argument("--project", type=Path, default=None)
    run_project(parser.parse_args())


if __name__ == "__main__":
    main()
