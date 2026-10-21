"Junta Server com Settings na camada service"

from WatchGuardian._internal.core.module import Settings
from WatchGuardian._internal.server.manage import Server


class WatchServer(Server):

    def __init__(self, settings: Settings) -> None:
        super().__init__(settings=settings)
