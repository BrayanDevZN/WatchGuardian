from src.logs.module import Logs
logger =Logs(loglevel="SUCCESS")

"""Cria engine do banco"""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine 
from sqlalchemy import text
class Engine:

    def __init__(self, url:str)-> None:

        self.url = url 

    #Cria a engine
    def _create(self) -> None:

        try:

            logger.info("Criando engine do banco de dados...")

            self.eng = create_async_engine(url=self.url)

            logger.success("Engine criada!!")

        except Exception as error:

            logger.error(f"Erro ao criar engine: {error}")
            raise 

    #testa
    async def _test(self) -> None:

        countdown = 0
        while True:
            try:

                logger.info("Testando conexão do banco de dados...")

                async with self.eng.begin() as session:

                    await session.execute(text("SELECT 1"))

                logger.success("Conexão testada com sucesso!!")
                break

            except Exception as error:

                if countdown != 3:

                    logger.warning("Houve um erro ao se conectar, testando conexão novamente...")
                    countdown+=1
                    continue

                logger.error(f"Houve um erro na conexão: {error}")

    #executa os metodos
    async def get_engine(self) -> AsyncEngine:

        self._create()
        await self._test()
        return self.eng

    

            

