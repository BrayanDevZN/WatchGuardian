from src.logs.module import Logs
logger =Logs(loglevel="SUCCESS")

"""
Cria orquestrador de sessoes
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine


def create_session(engine:AsyncEngine):

    try:

        logger.info("Criando orquestrador de sessão...")

        session = async_sessionmaker(engine, expire_on_commit=False)

        logger.success("Criado com sucesso!!")

        return session 

    except Exception as error:

        logger.error(f"Houve um erro ao criar orquestrador: {error}")