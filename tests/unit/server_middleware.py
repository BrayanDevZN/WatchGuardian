"""Tests Redis-backed HTTP rate limiting and its unavailable response."""

import asyncio

from fastapi import Request
from fastapi.responses import Response

from WatchGuardian._internal.core.module import Settings
from WatchGuardian._internal.server.midlleware import Midlleware


class FakeCache:
    def __init__(self) -> None:
        self.counts: dict[str, int] = {}

    async def read(self, key: str):
        return self.counts.get(key)

    async def incr(self, key: str):
        self.counts[key] = self.counts.get(key, 0) + 1
        return self.counts[key]


def make_request(host: str = "127.0.0.1") -> Request:
    return Request({
        "type": "http",
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": "/health/",
        "raw_path": b"/health/",
        "query_string": b"",
        "headers": [],
        "client": (host, 50000),
        "server": ("localhost", 8000),
    })


async def test_redis_http_limit_and_unavailable_response() -> None:
    settings = Settings()
    settings.secrets["rate_limit"] = "2"
    cache = FakeCache()
    middleware = Midlleware(app=lambda *_args: None, settings=settings, cache=cache)

    async def next_response(_request):
        return Response(status_code=200)

    assert (await middleware.dispatch(make_request(), next_response)).status_code == 200
    assert (await middleware.dispatch(make_request(), next_response)).status_code == 200
    assert (await middleware.dispatch(make_request(), next_response)).status_code == 429

    no_redis = Midlleware(app=lambda *_args: None, settings=settings, cache=None)
    unavailable = await no_redis.dispatch(make_request(), next_response)
    assert unavailable.status_code == 503


if __name__ == "__main__":
    asyncio.run(test_redis_http_limit_and_unavailable_response())
    print("Server middleware test passed")
