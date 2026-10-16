"""
Gerencia acesso aos dados por banco local ou HTTP com cache-aside opcional.
"""

from src.core.module import Settings, config_url
from src.database.manage import ControlDb
from src.service.cache import CacheManage
from src.service.client import ClientHttp

from .merge import MergeDb


class WatchDb(MergeDb):

    def __init__(self, settings: Settings, http: bool = False) -> None:
        self.settings = settings
        self.http = http
        self.control: ControlDb | ClientHttp

        if self.http:
            settings.add_secret(["url", "token"])
            settings.required_secrets("token")

            self.control = ClientHttp(settings=settings)
        else:
            settings.add_secret("url_db")

            url = settings.get_secret(secret_name="url_db")
            path = settings.get_config(name="path")
            url = config_url(url=url, path=path)

            self.control = ControlDb(url=url)

        settings.add_secret(["host", "port"])

        host = settings.get_secret(secret_name="host")
        port = settings.get_secret(secret_name="port")

        self.cache = None

        if host is not None and port is not None:
            self.cache = CacheManage(settings=settings)

    def _local_control(self) -> ControlDb:
        if not isinstance(self.control, ControlDb):
            raise RuntimeError(
                "Operacoes de migracao so podem ser executadas com banco local."
            )

        return self.control

    async def create_tables(self) -> None:
        await self._local_control().create_tables()

    async def reset_tables(self) -> None:
        await self._local_control().reset_tables()

    async def drop_tables(self) -> None:
        await self._local_control().drop_tables()

    async def _initializate(self) -> "WatchDb":
        if isinstance(self.control, ControlDb):
            await self.control.run()

        MergeDb.__init__(
            self,
            control=self.control,
            cache=self.cache,
        )

        return self

    def __await__(self):
        return self._initializate().__await__()
