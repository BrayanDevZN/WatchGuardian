"""
Junta os controles das tabelas de banco com cache opcional.
"""

from src.database.manage import ControlDb
from src.service.cache import CacheManage

from .logs import LogsService
from .obs import ObsService


class MergeDb:

    def __init__(self, control_db: ControlDb, cache: CacheManage | None = None) -> None:
        self.control_db = control_db
        self.cache = cache

        self.logs = LogsService(
            control_db=control_db,
            cache=cache,
        )

        self.observability = ObsService(
            control_db=control_db,
            cache=cache,
        )
