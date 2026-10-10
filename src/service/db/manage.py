"""
Gerencia banco e cache opcional para os services de tabelas.
"""

from src.core.module import Settings, config_url
from src.database.manage import ControlDb
from src.service.cache import CacheManage

from .merge import MergeDb


class WatchDb(ControlDb, MergeDb):

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

        url = settings.get_secret(secret_name="url")
        path = settings.get_config(name="path")
        url = config_url(url=url, path=path)

        ControlDb.__init__(self, url=url)

        host = settings.get_secret(secret_name="host")
        port = settings.get_secret(secret_name="port")

        self.cache = None

        if host is not None and port is not None:
            self.cache = CacheManage(settings=settings)

    async def _initializate(self) -> "WatchDb":
        await self.run()

        MergeDb.__init__(
            self,
            control_db=self,
            cache=self.cache,
        )

        return self

    def __await__(self):
        return self._initializate().__await__()
