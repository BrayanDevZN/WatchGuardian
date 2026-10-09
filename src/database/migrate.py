from src.logs.module import Logs
logger =Logs(loglevel="SUCCESS")


"Cria as tabelas do banco de dados"

from sqlalchemy.ext.asyncio import AsyncEngine
from src.database.base import Base 
from src.database.models.logs import ModelLogs
from src.database.models.observability import ModelObservability
from sqlalchemy import text

class Migrate:

    def __init__(self, engine:AsyncEngine)-> None:
        self.engine = engine
        
    async def create_tables(self) -> None:

        try:

            logger.info("Criando as tabelas se não existirem...")

            async with self.engine.begin() as session:

                await session.run_sync(Base.metadata.create_all)

            logger.success("Feito!!")

        except Exception as error:

            logger.error(f"Houve um erro ao criar: {error}")
            raise 

    #Deleta as tabelas
    async def drop_tables(self) -> None: 

        try:

            logger.info("Deletando tabelas...")

            async with self.engine.begin() as session:

                await session.run_sync(Base.metadata.drop_all)

            logger.success("Feito!!")

        except Exception as error:

            logger.error(f"Houve um erro ao deletar: {error}")
            raise 

    #Deleta os dados das tabelas
    async def reset_tables(self) -> None:

        try:

            logger.info("Resetando as tabelas...")

            async with self.engine.begin() as session:

                querys = [
                    "delete from logs",
                    "delete from observability"
                ]

                for query in querys:

                    sql = text(query)

               

                    await session.execute(sql)

            logger.success("Feito!!")

        except Exception as error:

            logger.error(f"Erro ao resetar:  {error}")
            raise
