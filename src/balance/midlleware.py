"Midlleware de balance"

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.replicator.module import Replicators, Replicator
from src.logs.module import Logs
import time
logger = Logs(loglevel="SUCCESS")
class Midlleware(BaseHTTPMiddleware):

    def __init__(self, app, instance:Replicators|list[Replicator], timeout:int=60)-> None:

        self.instance = instance
        self.timeout = timeout

        super().__init__(app)


    async def _get_instance(self) -> None:

        self.replicas = await self.instance.get_replicas() if isinstance(self.instance, Replicators) else self.instance

    #Valida qual instancia da api esta funcionando
    async def _valid(self, request:Request) -> None:

        logger.info(f"Choosing a replica...")
        start = time.monotonic()

        self.replica = None

        while time.monotonic() - start < self.timeout:



            for replica in self.replicas:



                valid = await replica.valid()

                if valid and request.method in replica.methods:
                    self.replica = replica.url
                    logger.success(f"Replica escolhida: {replica.url}")
                    break

            if self.replica is not None:
                break 

            continue

        raise HTTPException(
            detail="not valid replica",
            status_code=501
        )

    async def dispatch(self, request:Request, call_next):

       
        await self._get_instance()
        await self._valid(request=request)

        request.state.url = self.replica

        return await call_next(request)


        

            

            
                


        



       