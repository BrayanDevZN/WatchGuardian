"confere o rate limit"

from starlette.middleware.base import BaseHTTPMiddleware
from src.core.module import Settings
from src.service.cache import CacheManage
from fastapi import Request, HTTPException

class Midlleware(BaseHTTPMiddleware):

    def __init__(self, app, settings:Settings, cache:CacheManage, origin:str|list)-> None:
        super().__init__(app)

        self.settings = settings
        self.cache = cache
        self.origin = origin

    async def dispatch(self, request:Request, call_next):

        name = f"rate_limit:{request.client.host + request.client.port}"

        rate_limit = int(self.settings.required_secrets(secret="rate_limit"))
        
        user_limit = await self.cache.read(key=name)

        origin_url = request.headers.get("origin")

        

        if ((isinstance(self.origin, list) and user_limit is not None and user_limit > rate_limit and not origin_url in self.origin)or
            (isinstance(self.origin, str) and user_limit is not None and user_limit > rate_limit and origin_url != self.origin)
            ):

            raise HTTPException(
                status_code=429,
                detail="Too many requests"
            )

        await self.cache.incr(key=name)

        
        await call_next(request)
