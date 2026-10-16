from src.logs.module import Logs
logger = Logs(loglevel="SUCCESS")
"Contra a replcia especifica"
from src.core.module import Settings
from src.service.module import ClientHttp, CacheManage
class PathError(Exception):
    pass 
class MethodError(Exception):
    pass


class Replicator(ClientHttp):

    def __init__(self,url:str, cache:CacheManage,limit:int,name:str, paths:str|list="*", methods:str|list="*", limit_expires:int=60)->None:

     
        self.cache = cache
        self.name = name
        self.paths = paths 
        self.limit = limit 
        self.methods =methods
        self.expires= limit_expires
        self.url = url
        
        super().__init__(url=self.url)
        

    #Adiciona o limite
    async def _limit(self) -> None:

        await self.cache.incr(key=f"limit:{self.name}", time=self.expires)

    #pega o limite
    async def _get(self) -> None|int:

        result = await self.cache.read(key=f"limit:{self.name}")

        return int(result) if result is not None else None

    #Valida os paths
    async def _valid_paths(self) -> None:

        PATHS = ["logs", "obs", "*"]

        if self.paths == "*":

            return 

        for path in self.paths:

            if not path in PATHS:
                raise PathError(f"Not expeted path {path}")

        
    #Valida os metodos
    async def _valid_methods(self) -> None:

        METHODS = ["POST", "PATCH", "PUT", "GET", "DEELTE", "*"]

        if self.methods == "*":
            return

        for method in self.methods:
            if not method in METHODS:
                raise MethodError(f"not expeted method {method}")


    

    #Confere se o limite excedeu, se sim, retorna false, se não, conta na chave e retorna True
    async def _exceded(self) -> None:

        limit = await self._get()

        if limit is not None and int(limit) > self.limit:

            logger.warning(f"Exceded limit for instance {self.name}")
            self.exceded = False


        self.exceded = True

    #Confere a api
    async def _health(self) -> None:

        self.status = await self.health()

    

    #chama todos os metodos
    async def valid(self) ->bool:
        await self._valid_paths()
        await self._valid_methods()
        await self._exceded()
        await self._health()
        
        return self.exceded and self.status




    



    



    

    


        
        