"""
Junta os controles das tabelas com cache-aside opcional.
"""

from WatchGuardian._internal.database.manage import ControlDb
from WatchGuardian._internal.service.cache import CacheManage
from WatchGuardian._internal.service.client import ClientHttp

from .logs import LogsService
from .obs import ObsService


class MergeDb:

    def __init__(
        self,
        control: ControlDb | ClientHttp,
        cache: CacheManage | None = None,
    ) -> None:
        self.control = control
        self.cache = cache

        self.logs = LogsService(
            control=control,
            cache=cache,
        )

        self.observability = ObsService(
            control=control,
            cache=cache,
        )
