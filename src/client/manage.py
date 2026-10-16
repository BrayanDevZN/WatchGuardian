"Gerencia os clients das rotas do servidor"

from .auth import AuthClient, logger
from .logs import LogsClient
from .obs import ObsClient
import requests

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




