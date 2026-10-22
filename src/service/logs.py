"""Combine console logging with asynchronous database persistence."""

import asyncio
from typing import Literal

from .db import WatchDb
from src.logs.module import Logs


class WatchLogs:
    def __init__(
        self,
        loglevel: Literal["SUCCESS", "INFO", "WARNING", "ERROR", "DEBUG", "CRITICAL"] = "INFO",
        watch_db: WatchDb | None = None,
    ) -> None:
        self.db = watch_db
        self.logs = Logs(loglevel=loglevel)
        self._tasks: set[asyncio.Task[None]] = set()

    async def _save(self, text: str, status: str) -> None:
        if self.db is not None:
            await self.db.logs.create(log=text, status=status)

    def _task_finished(self, task: asyncio.Task[None]) -> None:
        self._tasks.discard(task)
        if task.cancelled():
            return
        error = task.exception()
        if error is not None:
            self.logs.error(f"Failed to save log to database: {error}")

    def _background_save(self, text: str, status: str) -> None:
        if self.db is None:
            return

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            self.logs.warning(
                "Database log persistence needs a running asyncio event loop; "
                "this log was written to the console only."
            )
            return

        task = loop.create_task(self._save(text=text, status=status))
        self._tasks.add(task)
        task.add_done_callback(self._task_finished)

    async def flush(self) -> None:
        """Wait for currently scheduled database writes to finish."""
        if self._tasks:
            await asyncio.gather(*tuple(self._tasks))

    def success(self, text: str) -> dict | None:
        data = self.logs.success(text=text)
        if data is not None:
            self._background_save(text=text, status="SUCCESS")
        return data

    def info(self, text: str) -> dict | None:
        data = self.logs.info(text=text)
        if data is not None:
            self._background_save(text=text, status="INFO")
        return data

    def warning(self, text: str) -> dict | None:
        data = self.logs.warning(text=text)
        if data is not None:
            self._background_save(text=text, status="WARNING")
        return data

    def error(self, text: str) -> dict | None:
        data = self.logs.error(text=text)
        if data is not None:
            self._background_save(text=text, status="ERROR")
        return data

    def debug(self, text: str) -> dict | None:
        data = self.logs.debug(text=text)
        if data is not None:
            self._background_save(text=text, status="DEBUG")
        return data

    def critical(self, text: str) -> dict | None:
        data = self.logs.critical(text=text)
        if data is not None:
            self._background_save(text=text, status="CRITICAL")
        return data
