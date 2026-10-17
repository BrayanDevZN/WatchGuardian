"Gerencia os clients das rotas do servidor"

from .auth import AuthClient, logger
from .logs import LogsClient
from .obs import ObsClient
import requests
import json
from collections.abc import AsyncIterator
from typing import Any
from urllib.parse import urlsplit, urlunsplit
from websockets.asyncio.client import connect

class Client:

    def __init__(self, url: str) -> None:
        self.url = url.rstrip("/")

    def logs(self, token: str) -> LogsClient:
        return LogsClient(
            url=self.url,
            token=token
        )

    def obs(self, token: str) -> ObsClient:
        return ObsClient(
            url=self.url,
            token=token
        )

    def auth(self, user_token: str, refresh_token: str) -> AuthClient:
        return AuthClient(
            url=self.url,
            user_token=user_token,
            refresh_token=refresh_token
        )

    async def _listen_events(self, path: str, token: str) -> AsyncIterator[dict[str, Any]]:
        parsed_url = urlsplit(self.url)
        scheme = {"http": "ws", "https": "wss"}.get(parsed_url.scheme, parsed_url.scheme)
        ws_url = urlunsplit((scheme, parsed_url.netloc, path, "", ""))

        async with connect(
            ws_url,
            additional_headers={"X-user_token": token},
        ) as websocket:
            async for message in websocket:
                event = json.loads(message)
                if not isinstance(event, dict):
                    raise ValueError("WebSocket event must be a JSON object")
                yield event

    async def listen_logs(self, token: str) -> AsyncIterator[dict[str, Any]]:
        """Yield log events from the authenticated `/logs/ws` WebSocket."""
        async for event in self._listen_events("/logs/ws", token):
            yield event

    async def listen_obs(self, token: str) -> AsyncIterator[dict[str, Any]]:
        """Yield observability events from the authenticated `/obs/ws` WebSocket."""
        async for event in self._listen_events("/obs/ws", token):
            yield event

    async def health(self) -> bool:

        countdown = 0

        while True:
            logger.info(f"Check health from {self.url}...")

            try:

                response = requests.get(url=self.url + "/health")
                if response.status_code > 400:
                    logger.error(f"Error: {response.text} | Status code: {response.text}")
                    return False

                logger.success(f"Connection from {self.url} ok!!")
                return True

            except requests.exceptions.ConnectionError:
                if countdown ==3:
                    logger.error("Connection recused")
                    return False
                    

                logger.warning("Connection recused, testing again...")
                countdown+=1
                continue




