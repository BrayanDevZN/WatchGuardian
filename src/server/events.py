"""In-process WebSocket event fan-out backed by optional Redis Pub/Sub."""

import asyncio
import json
import uuid
from collections import OrderedDict
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import AsyncIterator

from src.logs.module import Logs
from src.service.cache import CacheManage


logger = Logs(loglevel="INFO")


class RealtimeEvents:
    CHANNEL = "watchguardian:realtime"

    def __init__(self, cache: CacheManage | None = None) -> None:
        self.cache = cache
        self._subscribers: dict[asyncio.Queue[dict], str | None] = {}
        self._listener: asyncio.Task | None = None
        self._seen: OrderedDict[str, None] = OrderedDict()

    async def start(self) -> None:
        if self.cache is not None and self._listener is None:
            self._listener = asyncio.create_task(self._listen_redis())

    async def stop(self) -> None:
        if self._listener is None:
            return
        self._listener.cancel()
        try:
            await self._listener
        except asyncio.CancelledError:
            pass
        finally:
            self._listener = None

    @asynccontextmanager
    async def subscribe(self, prefix: str | None = None) -> AsyncIterator[asyncio.Queue[dict]]:
        queue: asyncio.Queue[dict] = asyncio.Queue(maxsize=256)
        self._subscribers[queue] = prefix
        try:
            yield queue
        finally:
            self._subscribers.pop(queue, None)

    async def publish(self, event_type: str, data: dict) -> dict:
        event = {
            "id": str(uuid.uuid4()),
            "type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data,
        }
        # Normalize datetimes and UUIDs before both local delivery and Redis
        # publication so the WebSocket JSON encoder receives serializable data.
        event = json.loads(json.dumps(event, default=str))

        # Always fan out locally. This also keeps the current process working
        # when Redis is absent or temporarily unavailable.
        await self._broadcast(event)

        if self.cache is not None:
            try:
                await self.cache.publish(
                    channel=self.CHANNEL,
                    event=json.dumps(event),
                )
            except Exception as error:
                logger.warning(f"Redis event publish failed; using local delivery: {error}")

        return event

    async def _listen_redis(self) -> None:
        while True:
            try:
                async for raw_event in self.cache.listen(self.CHANNEL):
                    if isinstance(raw_event, bytes):
                        raw_event = raw_event.decode("utf-8")
                    event = json.loads(raw_event)
                    await self._broadcast(event)
            except asyncio.CancelledError:
                raise
            except Exception as error:
                logger.warning(f"Redis event listener failed; retrying shortly: {error}")
                await asyncio.sleep(1)

    async def _broadcast(self, event: dict) -> None:
        event_id = event.get("id")
        if event_id is not None:
            if event_id in self._seen:
                return
            self._seen[event_id] = None
            if len(self._seen) > 2048:
                self._seen.popitem(last=False)

        for queue, prefix in tuple(self._subscribers.items()):
            if prefix is not None and not event.get("type", "").startswith(prefix):
                continue
            if queue.full():
                try:
                    queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass
            queue.put_nowait(event)
