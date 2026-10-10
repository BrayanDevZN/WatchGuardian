"""
Junta os modulos de db com settings e config
"""
from src.core.module import config_url, Settings
from src.database.manage import ControlDb


class WatchDb(ControlDb):
    def __init__(self, settings:Settings)-> None:

      
        url = settings.get_secret(secret_name="url")
        path = settings.get_config(name="path")

        url = config_url(url=url, path=path)
        super().__init__(url)

    async def _initializate(self) -> "WatchDb":

        await self.run()
        return self 

    def __await__(self):
        return self._initializate().__await__()

        
   
        

