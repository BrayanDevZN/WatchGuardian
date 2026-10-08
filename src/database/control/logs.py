"""
Controla a tabela logs.
"""

import uuid

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.logs import ModelLogs
from src.logs.module import Logs


logger = Logs(loglevel="SUCCESS")


class LogsDb:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def _to_dict(data: ModelLogs) -> dict:
        return {
            "id": data.id,
            "public_id": str(data.public_id),
            "log": data.log,
            "created_at": data.created_at,
        }

    async def create(self, log: str) -> dict:

        try:
            data = ModelLogs(
                log=log
            )

            self.session.add(data)

            await self.session.commit()
            await self.session.refresh(data)

            return self._to_dict(data)

        except Exception as error:
            await self.session.rollback()

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
            query = select(ModelLogs)

            if id is not None:
                query = query.where(
                    ModelLogs.id == id
                )

            elif public_id is not None:

                if isinstance(public_id, str):
                    public_id = uuid.UUID(public_id)

                query = query.where(
                    ModelLogs.public_id == public_id
                )

            result = await self.session.execute(query)

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
        log: str,
        id: int | None = None,
        public_id: uuid.UUID | str | None = None,
    ) -> dict | None:

        if id is None and public_id is None:
            raise ValueError(
                "Informe id ou public_id para atualizar o log."
            )

        try:
            query = (
                update(ModelLogs)
                .values(log=log)
                .returning(ModelLogs)
            )

            if id is not None:
                query = query.where(
                    ModelLogs.id == id
                )

            else:
                if isinstance(public_id, str):
                    public_id = uuid.UUID(public_id)

                query = query.where(
                    ModelLogs.public_id == public_id
                )

            result = await self.session.execute(query)

            data = result.scalar_one_or_none()

            if data is None:
                await self.session.rollback()
                return None

            await self.session.commit()

            return self._to_dict(data)

        except Exception as error:
            await self.session.rollback()

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
                    public_id = uuid.UUID(public_id)

                query = query.where(
                    ModelLogs.public_id == public_id
                )

            result = await self.session.execute(query)

            data = result.scalar_one_or_none()

            if data is None:
                await self.session.rollback()
                return None

            response = self._to_dict(data)

            await self.session.commit()

            return response

        except Exception as error:
            await self.session.rollback()

            logger.error(
                text=f"Erro ao deletar log: {error}"
            )

            raise