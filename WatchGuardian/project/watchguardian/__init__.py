"""Project template and module aggregator."""

from .manage import watch_manage
from .module import WatchModule
from .settings import ProjectSettings

__all__ = ["ProjectSettings", "WatchModule", "watch_manage"]
