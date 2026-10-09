"""
Junta db com logs
"""

import asyncio
from typing import Literal

from .db import WatchDb
from src.logs.module import Logs


class WatchLogs:

    def __init__(self, loglevel: Literal["SUCCESS", "INFO", "WARNING", "ERROR", "DEBUG", "CRITICAL"] = "INFO", watch_db: WatchDb | None = None) -> None:
        self.db = watch_db
        self.logs = Logs(loglevel=loglevel)
        self._tasks = set()

    async def _save(self, text: str, status: str) -> None:
        if self.db is not None:
            await self.db.logs.create(
                log=text,
                status=status
            )

    def _background_save(self, text: str, status: str) -> None:
        if self.db is None:
            return

        task = asyncio.create_task(
            self._save(
                text=text,
                status=status
            )
        )

        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    def success(self, text: str) -> dict | None:
        data = self.logs.success(text=text)

        if data is not None:
            self._background_save(
                text=text,
                status="SUCCESS"
            )

        return data

    def info(self, text: str) -> dict | None:
        data = self.logs.info(text=text)

        if data is not None:
            self._background_save(
                text=text,
                status="INFO"
            )

        return data

    def warning(self, text: str) -> dict | None:
        data = self.logs.warning(text=text)

        if data is not None:
            self._background_save(
                text=text,
                status="WARNING"
            )

        return data

    def error(self, text: str) -> dict | None:
        data = self.logs.error(text=text)

        if data is not None:
            self._background_save(
                text=text,
                status="ERROR"
            )

        return data

    def debug(self, text: str) -> dict | None:
        data = self.logs.debug(text=text)

        if data is not None:
            self._background_save(
                text=text,
                status="DEBUG"
            )

        return data

    def critical(self, text: str) -> dict | None:
        data = self.logs.critical(text=text)

        if data is not None:
            self._background_save(
                text=text,
                status="CRITICAL"
            )

        return data