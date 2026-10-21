"Cria as requisições para as rotas de logs"

import asyncio
from typing import Any, Literal

import requests

from WatchGuardian._internal.logs.module import Logs


logger = Logs(loglevel="SUCCESS")


class LogsClient:

    def __init__(self, url: str, token: str) -> None:
        self.url = f"{url.rstrip('/')}/logs/"
        self.headers = {
            "X-user_token": token
        }

    @staticmethod
    def _response(response: requests.Response) -> Any:
        if response.status_code >= 400:
            logger.error(f"Request failed with status {response.status_code}: {response.text}")
            return None

        return response.json()

    async def create_log(
        self,
        status: Literal[
            "SUCCESS",
            "INFO",
            "WARNING",
            "ERROR",
            "DEBUG",
            "CRITICAL"
        ],
        log: str
    ) -> Any:
        logger.info("Sending request to create log record...")

        content = {
            "status": status,
            "log": log
        }

        response = await asyncio.to_thread(
            requests.post,
            self.url,
            headers=self.headers,
            json=content
        )

        return self._response(response)

    async def get_log(self, id: int | None = None, public_id: str | None = None) -> Any:
        params = {
            key: value
            for key, value in {
                "id": id,
                "public_id": public_id
            }.items()
            if value is not None
        }

        response = await asyncio.to_thread(
            requests.get,
            self.url,
            headers=self.headers,
            params=params
        )

        return self._response(response)

    async def update_log(
        self,
        id: int | None = None,
        public_id: str | None = None,
        log: str | None = None,
        status: Literal[
            "SUCCESS",
            "INFO",
            "WARNING",
            "ERROR",
            "DEBUG",
            "CRITICAL"
        ] | None = None
    ) -> Any:
        params = {
            key: value
            for key, value in {
                "id": id,
                "public_id": public_id
            }.items()
            if value is not None
        }

        content = {
            "log": log,
            "status": status
        }

        response = await asyncio.to_thread(
            requests.patch,
            self.url,
            headers=self.headers,
            params=params,
            json=content
        )

        return self._response(response)

    async def delete_log(self, id: int | None = None, public_id: str | None = None) -> Any:
        params = {
            key: value
            for key, value in {
                "id": id,
                "public_id": public_id
            }.items()
            if value is not None
        }

        response = await asyncio.to_thread(
            requests.delete,
            self.url,
            headers=self.headers,
            params=params
        )

        return self._response(response)
