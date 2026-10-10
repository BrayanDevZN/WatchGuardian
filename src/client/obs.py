"Cria as requisições para as rotas de observabilidade"

import asyncio
from typing import Any, Literal

import requests

from src.logs.module import Logs


logger = Logs(loglevel="SUCCESS")


class ObsClient:

    def __init__(self, url: str, token: str) -> None:

        self.url = f"{url.rstrip('/')}/obs/"
        self.headers = {
            "X-user_token": token
        }

    @staticmethod
    def _response(response: requests.Response) -> Any:

        if response.status_code >= 400:
            logger.error(
                f"Houve um erro de status {response.status_code}: {response.text}"
            )
            return None

        return response.json()

    async def create_obs(
        self,
        task: str,
        status: Literal["sucess", "pending", "failure"],
        content: str,
        latency: int
    ) -> Any:

        data = {
            "task": task,
            "status": status,
            "content": content,
            "latency": latency
        }

        response = await asyncio.to_thread(
            requests.post,
            self.url,
            headers=self.headers,
            json=data
        )

        return self._response(response)

    async def get_obs(
        self,
        id: int | None = None,
        public_id: str | None = None
    ) -> Any:

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

    async def update_obs(
        self,
        id: int | None = None,
        public_id: str | None = None,
        task: str | None = None,
        status: Literal["sucess", "pending", "failure"] | None = None,
        content: str | None = None,
        latency: int | None = None
    ) -> Any:

        params = {
            key: value
            for key, value in {
                "id": id,
                "public_id": public_id
            }.items()
            if value is not None
        }

        data = {
            "task": task,
            "status": status,
            "content": content,
            "latency": latency
        }

        response = await asyncio.to_thread(
            requests.patch,
            self.url,
            headers=self.headers,
            params=params,
            json=data
        )

        return self._response(response)

    async def delete_obs(
        self,
        id: int | None = None,
        public_id: str | None = None
    ) -> Any:

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
