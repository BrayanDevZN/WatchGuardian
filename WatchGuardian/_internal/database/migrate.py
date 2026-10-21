from WatchGuardian._internal.logs.module import Logs
logger = Logs(loglevel="SUCCESS")

"Cria as tabelas do banco de dados"

from sqlalchemy.ext.asyncio import AsyncEngine
from WatchGuardian._internal.database.base import Base
from WatchGuardian._internal.database.models.logs import ModelLogs
from WatchGuardian._internal.database.models.observability import ModelObservability
from sqlalchemy import text, inspect


class Migrate:

    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine

    async def create_tables(self) -> None:
        try:
            logger.info("Creating database tables if they do not exist...")

            async with self.engine.begin() as session:
                await session.run_sync(Base.metadata.create_all)
                # create_all does not add columns to tables created by older releases.
                def add_memory_bytes_column(connection) -> None:
                    columns = {column["name"] for column in inspect(connection).get_columns("observability")}
                    if "memory_bytes" not in columns:
                        connection.exec_driver_sql(
                            "ALTER TABLE observability ADD COLUMN memory_bytes INTEGER NOT NULL DEFAULT 0"
                        )

                await session.run_sync(add_memory_bytes_column)

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
