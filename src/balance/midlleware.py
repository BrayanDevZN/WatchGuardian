"""Middleware responsável por escolher uma réplica saudável."""

import asyncio
import time

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.logs.module import Logs
from src.replicator.module import Replicator, Replicators


logger = Logs(loglevel="SUCCESS")


class Midlleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        instance: Replicators | list[Replicator],
        timeout: int = 60,
    ) -> None:
        self.instance = instance
        self.timeout = timeout
        super().__init__(app)

    async def _get_instance(self) -> None:
        self.replicas = (
            await self.instance.get_replicas()
            if isinstance(self.instance, Replicators)
            else self.instance
        )

    async def _valid(self, request: Request) -> None:
        logger.info("Choosing a replica...")
        start = time.monotonic()

        while time.monotonic() - start < self.timeout:
            for replica in self.replicas:
                try:
                    valid = await replica.valid()
                except Exception as error:
                    logger.warning(f"Failed to validate {replica.url}: {error}")
                    continue

                methods = replica.methods
                method_allowed = methods == "*" or request.method in methods
                if valid and method_allowed:
                    self.replica = replica.url
                    logger.success(f"Replica escolhida: {replica.url}")
                    return

            await asyncio.sleep(0.1)

        raise HTTPException(
            detail="not valid replica",
            status_code=501,
        )

    async def dispatch(self, request: Request, call_next):
        await self._get_instance()
        await self._valid(request=request)

        request.state.url = self.replica
        return await call_next(request)
