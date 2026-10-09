"""
Controla a tabela logs.
"""

import uuid
from typing import Literal

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.database.models.logs import ModelLogs
from src.logs.module import Logs


logger = Logs(loglevel="SUCCESS")

LogStatus = Literal[
    "SUCCESS",
    "INFO",
    "WARNING",
    "ERROR",
    "DEBUG",
    "CRITICAL",
]


class LogsDb:

    def __init__(
        self,
        session: async_sessionmaker[AsyncSession]
    ) -> None:
        self.session = session

    @staticmethod
    def _to_dict(data: ModelLogs) -> dict:
        return {
            "id": data.id,
            "public_id": str(data.public_id),
            "log": data.log,
            "status": data.status,
            "created_at": data.created_at,
        }

    async def create(
        self,
        log: str,
        status: LogStatus
    ) -> dict:

        try:

            async with self.session.begin() as session:

                data = ModelLogs(
                    log=log,
                    status=status
                )

                session.add(data)

                await session.flush()
                await session.refresh(data)

                return self._to_dict(data)

        except Exception as error:

            logger.error(
                text=f"Erro ao criar log: {error}"
            )

            raise

    async def select(
        self,
        id: int | None = None,
        public_id: uuid.UUID | str | None = None,
    ) -> dict | list[dict] | None:

        try:

            async with self.session.begin() as session:

                query = select(ModelLogs)

                if id is not None:

                    query = query.where(
                        ModelLogs.id == id
                    )

                elif public_id is not None:

                    if isinstance(public_id, str):
                        public_id = uuid.UUID(
                            public_id
                        )

                    query = query.where(
                        ModelLogs.public_id == public_id
                    )

                result = await session.execute(
                    query
                )

                if id is None and public_id is None:

                    logs = result.scalars().all()

                    return [
                        self._to_dict(log)
                        for log in logs
                    ]

                log = result.scalar_one_or_none()

                if log is None:
                    return None

                return self._to_dict(log)

        except Exception as error:

            logger.error(
                text=f"Erro ao buscar logs: {error}"
            )

            raise

    async def update(
        self,
        id: int | None = None,
        public_id: uuid.UUID | str | None = None,
        log: str | None = None,
        status: LogStatus | None = None,
    ) -> dict | None:

        if id is None and public_id is None:

            raise ValueError(
                "Informe id ou public_id para atualizar o log."
            )

        values = {}

        if log is not None:
            values["log"] = log

        if status is not None:
            values["status"] = status

        if not values:

            raise ValueError(
                "Informe log ou status para atualizar."
            )

        try:

            async with self.session.begin() as session:

                query = (
                    update(ModelLogs)
                    .values(**values)
                    .returning(ModelLogs)
                )

                if id is not None:

                    query = query.where(
                        ModelLogs.id == id
                    )

                else:

                    if isinstance(public_id, str):
                        public_id = uuid.UUID(
                            public_id
                        )

                    query = query.where(
                        ModelLogs.public_id == public_id
                    )

                result = await session.execute(
                    query
                )

                data = result.scalar_one_or_none()

                if data is None:
                    return None

                return self._to_dict(data)

        except Exception as error:

            logger.error(
                text=f"Erro ao atualizar log: {error}"
            )

            raise

    async def delete(
        self,
        id: int | None = None,
        public_id: uuid.UUID | str | None = None,
    ) -> dict | None:

        if id is None and public_id is None:

            raise ValueError(
                "Informe id ou public_id para deletar o log."
            )

        try:

            async with self.session.begin() as session:

                query = (
                    delete(ModelLogs)
                    .returning(ModelLogs)
                )

                if id is not None:

                    query = query.where(
                        ModelLogs.id == id
                    )

                else:

                    if isinstance(public_id, str):
                        public_id = uuid.UUID(
                            public_id
                        )

                    query = query.where(
                        ModelLogs.public_id == public_id
                    )

                result = await session.execute(
                    query
                )

                data = result.scalar_one_or_none()

                if data is None:
                    return None

                return self._to_dict(data)

        except Exception as error:

            logger.error(
                text=f"Erro ao deletar log: {error}"
            )

            raise