"""Unit tests for the authenticated realtime client stream."""

import asyncio
import json
from unittest.mock import patch

from src.client.manage import Client
from src.server.events import RealtimeEvents


class FakeWebSocket:
    def __init__(self, event_type: str) -> None:
        self.messages = iter([json.dumps({"type": event_type, "data": {"id": 1}})])

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.messages)
        except StopIteration:
            raise StopAsyncIteration


class FakeConnection:
    def __init__(self, event_type: str) -> None:
        self.event_type = event_type

    async def __aenter__(self):
        return FakeWebSocket(self.event_type)

    async def __aexit__(self, *_args):
        return None


async def test_client_stream(path: str, method_name: str, event_type: str) -> None:
    with patch("src.client.manage.connect", return_value=FakeConnection(event_type)) as connect_mock:
        client = Client("https://watchguardian.example/base")
        stream = getattr(client, method_name)("test-token")
        events = [event async for event in stream]

    assert events == [{"type": event_type, "data": {"id": 1}}]
    connect_mock.assert_called_once_with(
        f"wss://watchguardian.example{path}",
        additional_headers={"X-user_token": "test-token"},
    )


async def test_event_stream_filters() -> None:
    hub = RealtimeEvents()
    async with hub.subscribe(prefix="logs.") as logs_queue:
        async with hub.subscribe(prefix="observability.") as obs_queue:
            await hub.publish("logs.created", {"id": 1})
            await hub.publish("observability.created", {"id": 2})

            assert (await logs_queue.get())["type"] == "logs.created"
            assert (await obs_queue.get())["type"] == "observability.created"
            assert logs_queue.empty()
            assert obs_queue.empty()


if __name__ == "__main__":
    asyncio.run(test_client_stream("/logs/ws", "listen_logs", "logs.created"))
    asyncio.run(test_client_stream("/obs/ws", "listen_obs", "observability.created"))
    asyncio.run(test_event_stream_filters())
    print("Realtime client test passed")
