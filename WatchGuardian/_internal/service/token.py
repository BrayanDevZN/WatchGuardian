"junta settings com token"

from datetime import datetime, timedelta, timezone
import uuid

from WatchGuardian._internal.core.module import Settings
from WatchGuardian._internal.auth.token import JWT, logger


class WatchAuth(JWT):

    def __init__(self, settings: Settings | None = None) -> None:
        secret = settings.get_secret("secret") if settings is not None else None

        if secret is not None:
            super().__init__(secret)

    def secret(self) -> str:
        logger.info("Generating secret...")

        secret = f"{uuid.uuid4()}{uuid.uuid4()}"

        logger.success("Secret generated successfully.")
        return secret

    async def user_token(self, payload: dict | None = None) -> str:
        exp = datetime.now(timezone.utc) + timedelta(hours=1)

        token_payload = dict(payload or {})
        token_payload["exp"] = int(exp.timestamp())
        token_payload["type"] = "user_token"

        return await self.encode(payload=token_payload)

    async def refresh_token(self, payload: dict | None = None) -> str:
        token_payload = dict(payload or {})
        token_payload.pop("exp", None)
        token_payload["type"] = "refresh_token"

        return await self.encode(payload=token_payload)
