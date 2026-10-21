"junta redis com settings"

from WatchGuardian._internal.cache.manage import RedisManage
from WatchGuardian._internal.core.module import Settings

class CacheManage(RedisManage):

    def __init__(self, settings:Settings)-> None:

        host = settings.required_secrets(secret="host")
        port = settings.required_secrets(secret="port")
        password = settings.get_secret(secret_name="password")

        super().__init__(host=host, port=port, password=password)
        