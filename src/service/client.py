"Junta o client HTTP com Settings"

from src.client.manage import Client
from src.core.module import Settings


class ClientHttp(Client):

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

        self.settings.add_secret("url")
        url = self.settings.get_secret(secret_name="url")

        if url is None:
            url = "http://localhost:8000"

        super().__init__(url=url)
