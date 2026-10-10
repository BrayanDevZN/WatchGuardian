"Junta o client HTTP com Settings"

from src.client.manage import Client
from src.core.module import Settings


class ClientHttp(Client):

    def __init__(self, settings: Settings, url: str | None = None) -> None:
        self.settings = settings

        if url is None:
            url = "http://localhost:8000"

        super().__init__(url=url)
