"confere o rate limit"

from starlette.middleware.base import BaseHTTPMiddleware
from WatchGuardian._internal.core.module import Settings
from WatchGuardian._internal.service.cache import CacheManage
from fastapi import Request
from fastapi.responses import JSONResponse

class Midlleware(BaseHTTPMiddleware):

    def __init__(self, app, settings: Settings, cache: CacheManage | None) -> None:
        super().__init__(app)

        self.settings = settings
        self.cache = cache

    async def dispatch(self, request:Request, call_next):

        client_host = request.client.host if request.client else "unknown"
        name = f"rate_limit:{client_host}"

        rate_limit = int(self.settings.required_secrets(secret="rate_limit"))
        
        if self.cache is None:
            return JSONResponse(
                status_code=503,
                content={"detail": "Redis rate limiter is unavailable"},
            )

        try:
            user_limit = await self.cache.read(key=name)
            if user_limit is not None and int(user_limit) >= rate_limit:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many requests"},
                )

            await self.cache.incr(key=name)
        except Exception:
            return JSONResponse(
                status_code=503,
                content={"detail": "Redis rate limiter is unavailable"},
            )

        return await call_next(request)
