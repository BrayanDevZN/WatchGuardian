"gera o token jwt"

from WatchGuardian._internal.logs.module import Logs
logger = Logs(loglevel="SUCCESS")

import jwt
from jwt.exceptions import InvalidSignatureError


class JWT:

    def __init__(self, secret: str) -> None:
        self.secret = secret
        self.alg = "HS256"

    async def encode(self, payload: dict) -> str:
        try:
            logger.info("Creating token...")

            token = jwt.encode(
                key=self.secret,
                algorithm=self.alg,
                payload=payload
            )

            logger.success("Token created successfully.")
            return token

        except Exception as error:
            logger.error(f"Failed to create token: {error}")
            raise

    async def decode(self, token: str) -> dict:
        try:
            logger.info("Decoding token...")

            payload = jwt.decode(
                key=self.secret,
                algorithms=self.alg,
                jwt=token
            )

            logger.success("Token decoded successfully.")
            return payload

        except InvalidSignatureError as error:
            logger.error(f"Failed to decode token: {error}")
            raise
