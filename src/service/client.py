"Junta o client HTTP com Settings"

from src.client.manage import Client
from src.core.module import Settings


class ClientHttp(Client):

    def __init__(self, settings: Settings|None=None, url:str|None=None) -> None:

        if settings is not None:
        
            settings.add_secret("url")
            url = settings.get_secret(secret_name="url")

        elif settings is None and url is None:

            url = "http://localhost:8000"

        

        super().__init__(url=url)
