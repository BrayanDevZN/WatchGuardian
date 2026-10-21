"""Tests that CLI project loading initializes only requested modules."""

import asyncio
from pathlib import Path
from unittest.mock import patch

import WatchGuardian._internal.cli.project as project_cli


class FakeProjectApp:
    def __init__(self) -> None:
        self.project_config = {"loglevel": "INFO"}
        self.settings_path = Path("main.py")
        self.settings = None
        self.module = None
        self.http = None


class FakeWatchModule:
    def __init__(self, *, settings, http, loglevel) -> None:
        self.calls = []
        self.settings = settings
        self.http = http
        self.loglevel = loglevel
        self.watch_db = None
        self.watch_logs = None
        self.watch_obs = None
        self.watch_auth = None
        self.cache = None
        self.client_http = None
        self.watch_server = None
        self.server_app = None
        self.replicators = None
        self.watch_balance = None
        self.balance_app = None

    async def database(self):
        self.calls.append("database")

    async def logs(self):
        self.calls.append("logs")

    async def observability(self):
        self.calls.append("observability")

    def auth(self):
        self.calls.append("auth")

    async def cache_module(self):
        self.calls.append("cache")

    def client(self):
        self.calls.append("client")

    def server(self):
        self.calls.append("server")

    def replica_module(self):
        self.calls.append("replicators")

    def balance(self):
        self.calls.append("balance")


WatchModule = FakeWatchModule


def test_project_loader_starts_only_requested_server_module() -> None:
    app = FakeProjectApp()

    with (
        patch.object(project_cli, "load_project_app", return_value=app),
        patch.object(project_cli, "load_project_settings", return_value="settings"),
    ):
        module = asyncio.run(
            project_cli.load_project_modules("project", ("server",))
        )

    assert module.calls == ["server"]
    assert app.module is module


def test_project_loader_starts_only_requested_replicators_module() -> None:
    app = FakeProjectApp()

    with (
        patch.object(project_cli, "load_project_app", return_value=app),
        patch.object(project_cli, "load_project_settings", return_value="settings"),
    ):
        module = asyncio.run(
            project_cli.load_project_modules("project", ("replicators",))
        )

    assert module.calls == ["replicators"]


if __name__ == "__main__":
    test_project_loader_starts_only_requested_server_module()
    test_project_loader_starts_only_requested_replicators_module()
    print("Selective project module tests passed")
