"""
Controla a tabela observability.
"""

import uuid

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.observability import ModelObservability
from src.logs.module import Logs


logger = Logs(loglevel="SUCCESS")


class ObservabilityDb:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def _to_dict(data: ModelObservability) -> dict:
        return {
            "id": data.id,
            "public_id": str(data.public_id),
            "status": data.status,
            "content": data.content,
            "created_at": data.created_at,
            "update_at": data.update_at,
        }

    async def create(
        self,
        status: str,
        content: str,
    ) -> dict:

        try:
            data = ModelObservability(
                status=status,
                content=content,
            )

            self.session.add(data)

            await self.session.commit()
            await self.session.refresh(data)

            return self._to_dict(data)

        except Exception as error:
            await self.session.rollback()

            logger.error(
                text=f"Erro ao criar observability: {error}"
            )

            raise

    async def select(
        self,
        id: int | None = None,
        public_id: uuid.UUID | str | None = None,
    ) -> dict | list[dict] | None:

        try:
            query = select(ModelObservability)

            if id is not None:
                query = query.where(
                    ModelObservability.id == id
                )

            elif public_id is not None:

                if isinstance(public_id, str):
                    public_id = uuid.UUID(public_id)

                query = query.where(
                    ModelObservability.public_id == public_id
                )

            result = await self.session.execute(query)

            if id is None and public_id is None:
                data = result.scalars().all()

                return [
                    self._to_dict(item)
                    for item in data
                ]

            data = result.scalar_one_or_none()

            if data is None:
                return None

            return self._to_dict(data)

        except Exception as error:

            logger.error(
                text=f"Erro ao buscar observability: {error}"
            )

            raise

    async def update(
        self,
        id: int | None = None,
        public_id: uuid.UUID | str | None = None,
        status: str | None = None,
        content: str | None = None,
    ) -> dict | None:

        if id is None and public_id is None:
            raise ValueError(
                "Informe id ou public_id para atualizar."
            )

        values = {}

        if status is not None:
            values["status"] = status

        if content is not None:
            values["content"] = content

        try:
            query = (
                update(ModelObservability)
                .values(**values)
                .returning(ModelObservability)
            )

            if id is not None:
                query = query.where(
                    ModelObservability.id == id
                )

            else:

                if isinstance(public_id, str):
                    public_id = uuid.UUID(public_id)

                query = query.where(
                    ModelObservability.public_id == public_id
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
                text=f"Erro ao atualizar observability: {error}"
            )

            raise

    async def delete(
        self,
        id: int | None = None,
        public_id: uuid.UUID | str | None = None,
    ) -> dict | None:

        if id is None and public_id is None:
            raise ValueError(
                "Informe id ou public_id para deletar."
            )

        try:
            query = (
                delete(ModelObservability)
                .returning(ModelObservability)
            )

            if id is not None:
                query = query.where(
                    ModelObservability.id == id
                )

            else:

                if isinstance(public_id, str):
                    public_id = uuid.UUID(public_id)

                query = query.where(
                    ModelObservability.public_id == public_id
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
                text=f"Erro ao deletar observability: {error}"
            )

            raise