"Junta Server com Settings na camada service"

from src.core.module import Settings
from src.server.manage import Server


class WatchServer(Server):

    def __init__(self, settings: Settings) -> None:
        super().__init__(settings=settings)
