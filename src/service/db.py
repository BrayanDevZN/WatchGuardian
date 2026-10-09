"""
Junta os modulos de db com config
"""
from src.core.module import config_url, Settings
from src.database.manage import ControlDb


class WatchDb(ControlDb):
    def __init__(self, url:str=None, path:str|None=None)-> None:

        url = config_url(url=url, path=path)
        super().__init__(url)
        

async def Control_db(url:str|None=None, path:str|None=None) -> ControlDb:

    url = config_url(url=url, path=path)

    instance = ControlDb(url=url)
    await instance.run()
    return instance