from ..logs.module import Logs
logger =Logs(loglevel="SUCCESS")
import os
"""
Configura como vai ser a url do banco
"""

def config_url(url:str|None=None, path:str|None=None) -> str:

     if url is not None:

            return url 

     if path is None:

            return "sqlite+aiosqlite:///watch.db"

     if not os.path.exists(path):

            raise FileNotFoundError(f"{path} não existe")

     return f"sqlite+aiosqlite:///{path if "/" == path[-1] else path + "/"}watch.db"

        

