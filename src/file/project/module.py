"Junta varios modulos com settings"
from WatchGuardian import Settings, WatchLogs, WatchAuth, WatchObs
from WatchGuardian.database import WatchDb, CacheManage
from WatchGuardian.server import WatchServer, ClientHttp
from WatchGuardian.balance import WatchBalance, Replicator, Replicators

class WatchModule:

    def __init__(self, settings:Settings)-> None:

        self.settings = settings

    
        