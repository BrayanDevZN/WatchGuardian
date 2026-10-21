"Inicia a api"
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from WatchGuardian._internal.auth.token import logger
from WatchGuardian._internal.core.module import Settings
from WatchGuardian._internal.service.cache import CacheManage
from .midlleware import Midlleware
from .handles.logs import logs_router
from .handles.obs import obs_router
from .handles.auth import auth_router
from .handles.health import health_router
from .handles.ws import realtime_router
from .events import RealtimeEvents


class Server:

    def __init__(self, settings: Settings) -> None:
        self.routes = [logs_router, obs_router, auth_router, health_router, realtime_router]
        self.settings = settings
        self.settings.add_secret(["host", "port"])
        self.cache = None
        if self.settings.get_secret("host") and self.settings.get_secret("port"):
            try:
                self.cache = CacheManage(settings=self.settings)
            except Exception as error:
                logger.warning(f"Redis unavailable; using local event delivery: {error}")
        self.events = RealtimeEvents(cache=self.cache)
        self.app = FastAPI(lifespan=self._lifespan)
        self.app.state.settings = settings
        self.app.state.allowed_origins = []
        self.app.state.realtime_events = self.events

    @asynccontextmanager
    async def _lifespan(self, app: FastAPI) -> AsyncIterator[None]:
        await self.events.start()
        try:
            yield
        finally:
            await self.events.stop()

    def _cors(self) -> None:
        logger.info("Creating CORS configuration...")

        origin = self.settings.required_secrets(secret="origin")
        self.origin = list(origin) if "[" in origin else origin
        self.app.state.allowed_origins = (
            self.origin if isinstance(self.origin, list) else [self.origin]
        )

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.origin,
            allow_headers=["*"],
            allow_methods=["*"]
        )

        logger.success("CORS configuration created successfully.")

    def _router(self) -> None:
        logger.info("Adding routes...")

        for router in self.routes:
            self.app.include_router(router=router)

        logger.success("Routes added successfully.")

    def _midlle(self) -> None:
        logger.info("Creating middleware...")

        self.app.add_middleware(
            Midlleware,
            settings=self.settings,
            cache=self.cache,
        )

        logger.success("Middleware created successfully.")

    def run(self) -> FastAPI:
        logger.info("Starting server...")

        self._cors()
        self._router()
        self._midlle()

        logger.success("Server started successfully.")
        return self.app
