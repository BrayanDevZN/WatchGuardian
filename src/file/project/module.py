"""Inicializa os módulos públicos do WatchGuardian com as mesmas Settings."""

from fastapi import FastAPI

from WatchGuardian import Settings, WatchLogs, WatchAuth, WatchObs
from WatchGuardian.database import WatchDb, CacheManage
from WatchGuardian.server import WatchServer, ClientHttp
from WatchGuardian.balance import WatchBalance, Replicators


class WatchModule:
    """Monta os módulos do framework respeitando suas dependências."""

    def __init__(
        self,
        settings: Settings,
        http: bool | None = None,
        loglevel: str = "INFO",
    ) -> None:
        self.settings = settings
        self.http = http
        self.loglevel = loglevel
        self.logger = WatchLogs(loglevel=loglevel)

        self.watch_db: WatchDb | None = None
        self.watch_logs: WatchLogs | None = None
        self.watch_obs: WatchObs | None = None
        self.watch_auth: WatchAuth | None = None
        self.cache: CacheManage | None = None
        self.client_http: ClientHttp | None = None
        self.watch_server: WatchServer | None = None
        self.server_app: FastAPI | None = None
        self.replicators: Replicators | None = None
        self.watch_balance: WatchBalance | None = None
        self.balance_app: FastAPI | None = None

        self.logger.info(
            f"WatchModule initialized (http={self.http}, loglevel={self.loglevel})."
        )

    async def database(self) -> WatchDb:
        """Inicializa WatchDb com o modo HTTP opcional."""
        if self.watch_db is None:
            self.logger.info(f"Initializing WatchDb (http={self.http}).")
            self.watch_db = await WatchDb(settings=self.settings, http=self.http)
            self.cache = self.watch_db.cache
            self.logger = WatchLogs(
                loglevel=self.loglevel,
                watch_db=self.watch_db,
            )
            self.logger.success("WatchDb initialized.")

        return self.watch_db

    async def logs(self) -> WatchLogs:
        """Cria WatchLogs ligado ao WatchDb."""
        if self.watch_logs is None:
            watch_db = await self.database()
            self.logger.info("Initializing WatchLogs.")
            self.watch_logs = WatchLogs(
                loglevel=self.loglevel,
                watch_db=watch_db,
            )
            self.logger.success("WatchLogs initialized.")

        return self.watch_logs

    async def observability(self) -> WatchObs:
        """Cria WatchObs com as instâncias compartilhadas de logs e banco."""
        if self.watch_obs is None:
            watch_db = await self.database()
            watch_logs = await self.logs()
            self.logger.info("Initializing WatchObs.")
            self.watch_obs = WatchObs(
                logs=watch_logs,
                watch_db=watch_db,
            )
            self.logger.success("WatchObs initialized.")

        return self.watch_obs

    def auth(self) -> WatchAuth:
        """Cria WatchAuth usando as Settings fornecidas."""
        if self.watch_auth is None:
            self.logger.info("Initializing WatchAuth.")
            self.watch_auth = WatchAuth(settings=self.settings)
            self.logger.success("WatchAuth initialized.")

        return self.watch_auth

    async def cache_module(self) -> CacheManage | None:
        """Expõe o cache que WatchDb já inicializou, quando disponível."""
        if self.cache is None and self.watch_db is None:
            await self.database()

        self.logger.info(
            "Cache is available." if self.cache is not None else "Cache is not configured."
        )
        return self.cache

    def client(self) -> ClientHttp:
        """Cria ClientHttp usando as Settings compartilhadas."""
        if self.client_http is None:
            self.logger.info("Initializing ClientHttp.")
            self.client_http = ClientHttp(settings=self.settings)
            self.logger.success("ClientHttp initialized.")

        return self.client_http

    def server(self) -> WatchServer:
        """Cria WatchServer e executa run() para obter a aplicação FastAPI."""
        if self.watch_server is None:
            self.logger.info("Initializing WatchServer.")
            self.watch_server = WatchServer(settings=self.settings)
            self.server_app = self.watch_server.run()
            self.logger.success("WatchServer initialized and started.")

        return self.watch_server

    def balance(self) -> WatchBalance:
        """Cria Replicators e executa WatchBalance para obter a aplicação."""
        if self.watch_balance is None:
            self.logger.info("Initializing Replicators.")
            self.replicators = Replicators(settings=self.settings)
            self.logger.success("Replicators initialized.")

            self.logger.info("Initializing WatchBalance.")
            self.watch_balance = WatchBalance(replicas=self.replicators)
            self.balance_app = self.watch_balance.run()
            self.logger.success("WatchBalance initialized and started.")

        return self.watch_balance

    async def load_modules(self) -> "WatchModule":
        """Inicializa todos os módulos e executa os apps de servidor e balance."""
        self.logger.info("Loading WatchGuardian modules.")

        await self.database()
        await self.logs()
        await self.observability()
        self.auth()
        await self.cache_module()
        self.client()
        self.server()
        self.balance()

        self.logger.success("All WatchGuardian modules have been loaded.")
        return self
