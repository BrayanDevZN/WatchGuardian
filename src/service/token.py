"junta settings com token"

from datetime import datetime, timedelta, timezone
import uuid

from src.core.module import Settings
from src.auth.token import JWT, logger


class WatchAuth(JWT):

    def __init__(self, settings: Settings | None = None) -> None:

        secret = settings.get_secret("secret") if settings is not None else None

        if secret is not None:
            super().__init__(secret)

    # Gera uma secret se prescisar
    def secret(self) -> str:

        logger.info("Gerando uma secret...")

        secret = str(uuid.uuid4())

        logger.success("Secret gerada com sucesso!!")

        return secret

    # Gera token de usuario com expiracao automatica em UTC
    async def user_token(self, payload: dict | None = None) -> str:

        exp = datetime.now(timezone.utc) + timedelta(hours=1)

        token_payload = dict(payload or {})
        token_payload["exp"] = int(exp.timestamp())
        token_payload["type"] = "user_token"

        return await self.encode(payload=token_payload)

    # Gera refresh token sem expiracao
    async def refresh_token(self, payload: dict | None = None) -> str:

        token_payload = dict(payload or {})
        token_payload.pop("exp", None)
        token_payload["type"] = "refresh_token"

        return await self.encode(payload=token_payload)
