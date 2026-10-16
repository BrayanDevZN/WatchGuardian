from src.logs.module import Logs
logger = Logs(loglevel="SUCCESS")

"Cria as tabelas do banco de dados"

from sqlalchemy.ext.asyncio import AsyncEngine
from src.database.base import Base
from src.database.models.logs import ModelLogs
from src.database.models.observability import ModelObservability
from sqlalchemy import text


class Migrate:

    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine

    async def create_tables(self) -> None:
        try:
            logger.info("Creating database tables if they do not exist...")

            async with self.engine.begin() as session:
                await session.run_sync(Base.metadata.create_all)

            logger.success("Database tables created successfully.")

        except Exception as error:
            logger.error(f"Failed to create database tables: {error}")
            raise

    async def drop_tables(self) -> None:
        try:
            logger.info("Dropping database tables...")

            async with self.engine.begin() as session:
                await session.run_sync(Base.metadata.drop_all)

            logger.success("Database tables dropped successfully.")

        except Exception as error:
            logger.error(f"Failed to drop database tables: {error}")
            raise

    async def reset_tables(self) -> None:
        try:
            logger.info("Resetting database tables...")

            async with self.engine.begin() as session:
                querys = [
                    "delete from logs",
                    "delete from observability"
                ]

                for query in querys:
                    await session.execute(text(query))

            logger.success("Database tables reset successfully.")

        except Exception as error:
            logger.error(f"Failed to reset database tables: {error}")
            raise
