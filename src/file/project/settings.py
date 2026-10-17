"Cria toda a configuração do projeto"

from WatchGuardian import Settings, WatchLogs
import os 
settings = Settings()

"Configuração de CacheManage"
os.environ["host"] = "localhost"
os.environ["port"] = "6379"


class ProjectSettings:

    def __init__(self, env_file:str|None=None)-> None:

        self.settings = Settings(env_file=env_file)
        self.logs = WatchLogs()

    #adiciona as variaveis locais
    def local(self) -> None:

        self.logs.info("Add locale environment")

        "Configuração de CacheManage"
        os.environ["host"] = "localhost"
        os.environ["port"] = "6379"

        "configuração de jwt"
        




        