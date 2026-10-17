"""
junta obs com db
"""

import asyncio
import os
import sys
import time
import uuid

from src.service.logs import WatchLogs, WatchDb


def _process_rss_bytes() -> int:
    """Return current process RSS in bytes where the platform exposes it."""
    try:
        with open("/proc/self/statm", encoding="ascii") as statm:
            resident_pages = int(statm.read().split()[1])
        return resident_pages * os.sysconf("SC_PAGE_SIZE")
    except (OSError, IndexError, ValueError):
        # Stdlib fallback: process high-water RSS, rather than current RSS.
        try:
            import resource
        except ImportError:
            return 0
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return int(peak if sys.platform == "darwin" else peak * 1024)


class ObsControl:

    def __init__(self, logs: WatchLogs, watch_db: WatchDb) -> None:
        self.logs = logs
        self.control_db = watch_db
        self._task_db: asyncio.Task | None = None
        self._memory_monitor: asyncio.Task | None = None
        self._memory_start = 0
        self._memory_peak = 0

    async def task(self, name: str, group: str) -> uuid.UUID:
        self.name = name
        self.start = time.perf_counter()
        self._memory_start = _process_rss_bytes()
        self._memory_peak = self._memory_start
        self._memory_monitor = asyncio.create_task(self._monitor_memory())
        self.id = uuid.uuid4()

        self._task_db = asyncio.create_task(
            self.control_db.observability.create(
                group=group,
                status="pending",
                task=name,
                content="init",
                latency=0,
                memory_bytes=self._memory_start,
                public_id=self.id
            )
        )
        await self._task_db

        self.logs.info(f"Task '{name}' started.")

        return self.id

    async def _monitor_memory(self) -> None:
        while True:
            self._memory_peak = max(self._memory_peak, _process_rss_bytes())
            await asyncio.sleep(0.05)

    async def commit(self, content: str, error: bool = False) -> None:
        if self._memory_monitor is not None:
            self._memory_monitor.cancel()
            try:
                await self._memory_monitor
            except asyncio.CancelledError:
                pass
        self._memory_peak = max(self._memory_peak, _process_rss_bytes())
        memory_bytes = max(0, self._memory_peak - self._memory_start)

        if self._task_db is not None:
            await self._task_db

        end = time.perf_counter()
        latency = end - self.start

        await self.control_db.observability.update(
            public_id=self.id,
            content=content,
            status="success" if not error else "failure",
            latency=latency,
            memory_bytes=memory_bytes,
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
