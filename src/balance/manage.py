"Cria a api de balance"
from .midlleware import logger, Midlleware, Replicators, Replicator
from .router import router
from fastapi import FastAPI
class BalanceServer:

    def __init__(self, replicas:Replicators|list[Replicator], timeout:int=60)-> None:

        self.app = FastAPI()
        self.replicas = replicas
        self.timeout = timeout


    #Adiciona midlleware
    def _midle(self) -> None:

        logger.info("Adding midlleware in balance...")

        self.app.add_middleware(Midlleware, instance=self.replicas, timeout=self.timeout)

    #Adiciona rota
    def _router(self) -> None:

        logger.info("Creating router for Balance...")

        self.app.include_router(router=router)

    #chama os metodos
    def run(self) -> FastAPI:
        logger.info("Creating Balance...")

        self._midle()
        self._router()

        logger.success("balance created!!")

        return self.app
        
