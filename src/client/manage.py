"Gerencia os clients das rotas do servidor"

from .auth import AuthClient
from .logs import LogsClient
from .obs import ObsClient


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
