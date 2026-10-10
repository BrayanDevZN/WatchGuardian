"junta settings com token"

from datetime import datetime, timezone
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

        secret = str(uuid.uuid8())

        logger.success("Secret gerada com sucesso!!")

        return secret

    # Gera token de usuario com expiracao em UTC
    async def user_token(self, exp: datetime) -> str:

        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
        else:
            exp = exp.astimezone(timezone.utc)

        payload = {
            "exp": exp,
            "type": "user_token"
        }

        return await self.encode(payload=payload)

    # Gera refresh token sem expiracao
    async def refresh_token(self) -> str:

        payload = {
            "type": "refresh_token"
        }

        return await self.encode(payload=payload)
