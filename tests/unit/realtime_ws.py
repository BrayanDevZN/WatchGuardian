"""Tests authenticated server WebSocket handlers and channel isolation."""

import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace

from fastapi import WebSocketDisconnect

from src.core.module import Settings
from src.server.events import RealtimeEvents
from src.server.routes import realtime_router
from src.server.handles.ws import logs_websocket, obs_websocket
from src.service.token import WatchAuth


class FakeWebSocket:
    def __init__(self, path: str, token: str, settings: Settings, events: RealtimeEvents) -> None:
        self.headers = {"X-user_token": token}
        self.query_params = {}
        self.app = SimpleNamespace(
            state=SimpleNamespace(
                settings=settings,
                allowed_origins=[],
                realtime_events=events,
            )
        )
        self.accepted = asyncio.Event()
        self.closed: list[tuple[int, str | None]] = []
        self.incoming: asyncio.Queue[str] = asyncio.Queue()
        self.sent: asyncio.Queue[dict] = asyncio.Queue()
        self.path = path

    async def accept(self) -> None:
        self.accepted.set()

    async def close(self, code: int, reason: str | None = None) -> None:
        self.closed.append((code, reason))

    async def receive_text(self) -> str:
        message = await self.incoming.get()
        if message == "disconnect":
            raise WebSocketDisconnect()
        return message

    async def send_json(self, data: dict) -> None:
        await self.sent.put(data)


async def test_server_websocket_channels_and_auth() -> None:
    settings = Settings()
    settings.secrets["secret"] = "realtime-ws-test-secret-long-enough-for-hs256"
    token = await WatchAuth(settings=settings).user_token({"sub": "test"})
    events = RealtimeEvents()

    logs_ws = FakeWebSocket("/logs/ws", token, settings, events)
    obs_ws = FakeWebSocket("/obs/ws", token, settings, events)
    logs_task = asyncio.create_task(logs_websocket(logs_ws))
    obs_task = asyncio.create_task(obs_websocket(obs_ws))

    try:
        await asyncio.wait_for(
            asyncio.gather(logs_ws.accepted.wait(), obs_ws.accepted.wait()),
            timeout=1,
        )

        await events.publish("observability.created", {"id": 2})
        await events.publish(
            "logs.created",
            {"id": 1, "created_at": datetime.now(timezone.utc)},
        )

        logs_event = await asyncio.wait_for(logs_ws.sent.get(), timeout=1)
        obs_event = await asyncio.wait_for(obs_ws.sent.get(), timeout=1)
        assert logs_event["type"] == "logs.created"
        assert isinstance(logs_event["data"]["created_at"], str)
        assert obs_event["type"] == "observability.created"
        assert logs_ws.sent.empty()
        assert obs_ws.sent.empty()

        routes = {route.path for route in realtime_router.routes}
        assert routes == {"/logs/ws", "/obs/ws"}

        invalid_ws = FakeWebSocket("/logs/ws", "invalid-token", settings, events)
        await logs_websocket(invalid_ws)
        assert invalid_ws.closed[0][0] == 4401
    finally:
        await logs_ws.incoming.put("disconnect")
        await obs_ws.incoming.put("disconnect")
        await asyncio.gather(logs_task, obs_task)


if __name__ == "__main__":
    asyncio.run(test_server_websocket_channels_and_auth())
    print("Server WebSocket tests passed")
