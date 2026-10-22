"""
Junta os controles das tabelas com cache-aside opcional.
"""

from src.database.manage import ControlDb
from src.service.cache import CacheManage
from src.service.client import ClientHttp

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
