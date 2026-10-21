from WatchGuardian._internal.logs.module import Logs
logger = Logs(loglevel="SUCCESS")

"""Cria engine do banco"""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import text


class Engine:

    def __init__(self, url: str) -> None:
        self.url = url

    def _create(self) -> None:
        try:
            logger.info("Creating database engine...")
            self.eng = create_async_engine(url=self.url)
            logger.success("Database engine created successfully.")

        except Exception as error:
            logger.error(f"Failed to create database engine: {error}")
            raise

    async def _test(self) -> None:
        countdown = 0

        while True:
            try:
                logger.info("Testing database connection...")

                async with self.eng.begin() as session:
                    await session.execute(text("SELECT 1"))

                logger.success("Database connection tested successfully.")
                break

            except Exception as error:
                if countdown != 3:
                    logger.warning("Database connection failed. Retrying...")
                    countdown += 1
                    continue

                logger.error(f"Database connection failed: {error}")
                raise

    async def get_engine(self) -> AsyncEngine:
        self._create()
        await self._test()
        return self.eng
