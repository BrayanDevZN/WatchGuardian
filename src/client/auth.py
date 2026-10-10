"Cria as requisições para as rotas de autenticação"

import asyncio
from typing import Any

import requests

from src.logs.module import Logs


logger = Logs(loglevel="SUCCESS")


class AuthClient:

    def __init__(self, url: str, user_token: str, refresh_token: str) -> None:

        self.url = f"{url.rstrip('/')}/auth"
        self.headers = {
            "X-user_token": user_token,
            "X-refresh_token": refresh_token
        }

    @staticmethod
    def _response(response: requests.Response) -> Any:

        if response.status_code >= 400:
            logger.error(
                f"Houve um erro de status {response.status_code}: {response.text}"
            )
            return None

        return response.json()

    async def refresh(self) -> Any:

        response = await asyncio.to_thread(
            requests.post,
            f"{self.url}/refresh",
            headers=self.headers
        )

        return self._response(response)
