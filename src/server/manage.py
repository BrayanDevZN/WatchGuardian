"Inicia a api"
from src.auth.token import logger
from src.core.module import Settings
from src.service.cache import CacheManage
from .midlleware import Midlleware
from .handles.logs import logs_router
from .handles.obs import obs_router
from .handles.auth import auth_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

class Server:

    def __init__(self, settings:Settings)-> None:

        self.app = FastAPI()
        self.routes = [logs_router, obs_router, auth_router]

        self.app.state.settings = settings

        self.settings = settings

        self.cache = CacheManage(settings=self.settings)

    #Adiciona cors
    def _cors(self) -> None:

        logger.info("Criando configuração de cors...")

        origin = self.settings.required_secrets(secret="origin")
        origin = list(origin) if "[" in origin else origin 

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origin,
            allow_headers=["*"],
            allow_methods=["*"]
        )

        logger.success("configuração criada com sucesso!!")

    #Adiciona as rotas
    def _router(self) -> None:

        logger.info("Adicionando rotas...")

        for router in self.routes:
            self.app.include_router(router=router)

        logger.success("Rotas adicionadas!!")


    #Adiciona o midlleware
    def _midlle(self) -> None:

        logger.info("Criando midlleware...")

        self.app.add_middleware(
            Midlleware,
            settings=self.settings,
            cache=self.cache
        )

        logger.success("Midlleware criado!!")

    #chama todos os metodos e retorna o objeto do fastapi
    def run(self) -> FastAPI:

        logger.info("Iniciando servidor...")

        self._cors()
        self._router()
        self._midlle()

        logger.success("Servidor iniciado com sucesso!!")

        return self.app



        