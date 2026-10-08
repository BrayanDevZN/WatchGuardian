"""
Junta os modulos de db com config
"""
from src.config import config_url
from src.database.manage import ControlDb

async def Control_db(url:str|None=None, path:str|None=None) -> ControlDb:

    url = config_url(url=url, path=path)

    instance = ControlDb(url=url)
    await instance.run()
    return instance