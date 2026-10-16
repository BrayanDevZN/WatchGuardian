"""
junta obs com db
"""

import asyncio
import time
import uuid

from src.service.logs import WatchLogs, WatchDb


class ObsControl:

    def __init__(self, logs: WatchLogs, watch_db: WatchDb) -> None:
        self.logs = logs
        self.control_db = watch_db
        self._task_db: asyncio.Task | None = None

    async def task(self, name: str, group: str) -> uuid.UUID:
        self.name = name
        self.start = time.perf_counter()
        self.id = uuid.uuid4()

        self._task_db = asyncio.create_task(
            self.control_db.observability.create(
                group=group,
                status="pending",
                task=name,
                content="init",
                latency=0,
                public_id=self.id
            )
        )

        self.logs.info(f"Task '{name}' started.")

        return self.id

    async def commit(self, content: str, error: bool = False) -> None:
        if self._task_db is not None:
            await self._task_db

        end = time.perf_counter()
        latency = end - self.start

        await self.control_db.observability.update(
            public_id=self.id,
            content=content,
            status="success" if not error else "failure",
            latency=latency
        )

        if error:
            self.logs.error(f"Task '{self.name}' failed: {content}")
        else:
            self.logs.success(f"Task '{self.name}' completed successfully.")

    async def close(self) -> None:
        if self._task_db is not None:
            await self._task_db

        await self.control_db.observability.delete(public_id=self.id)

        self.logs.success(f"Task '{self.name}' closed.")
