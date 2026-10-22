"""
Controla a tabela observability.
"""

import uuid

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.database.models.observability import ModelObservability
from src.logs.module import Logs


logger = Logs(loglevel="SUCCESS")


class ObservabilityDb:

    def __init__(self, session: async_sessionmaker[AsyncSession]) -> None:
        self.session = session

    @staticmethod
    def _to_dict(data: ModelObservability) -> dict:
        return {
            "id": data.id,
            "public_id": str(data.public_id),
            "group": data.group,
            "task": data.task,
            "status": data.status,
            "content": data.content,
            "latency": data.latency,
            "memory_bytes": data.memory_bytes,
            "created_at": data.created_at,
            "update_at": data.update_at,
        }

    async def create(
        self,
        group: str,
        task: str,
        status: str,
        content: str,
        latency: int,
        public_id: uuid.UUID | None = None,
        memory_bytes: int = 0,
    ) -> dict:
        try:
            async with self.session.begin() as session:
                data = ModelObservability(
                    group=group,
                    task=task,
                    status=status,
                    content=content,
                    latency=latency,
                    memory_bytes=memory_bytes,
                    public_id=public_id if public_id is not None else uuid.uuid4(),
                )

                session.add(data)
                await session.flush()
                await session.refresh(data)
                return self._to_dict(data)

        except Exception as error:
            logger.error(text=f"Failed to create observability record: {error}")
            raise

    async def select(
        self,
        id: int | None = None,
        public_id: uuid.UUID | str | None = None,
        group: str | None = None,
    ) -> dict | list[dict] | None:
        try:
            async with self.session.begin() as session:
                query = select(ModelObservability)

                if id is not None:
                    query = query.where(ModelObservability.id == id)

                if public_id is not None:
                    if isinstance(public_id, str):
                        public_id = uuid.UUID(public_id)

                    query = query.where(ModelObservability.public_id == public_id)

                if group is not None:
                    query = query.where(ModelObservability.group == group)

                result = await session.execute(query)

                if id is None and public_id is None:
                    data = result.scalars().all()
                    return [self._to_dict(item) for item in data]

                data = result.scalar_one_or_none()

                if data is None:
                    return None

                return self._to_dict(data)

        except Exception as error:
            logger.error(text=f"Failed to fetch observability records: {error}")
            raise

    async def update(
        self,
        id: int | None = None,
        public_id: uuid.UUID | str | None = None,
        group: str | None = None,
        task: str | None = None,
        status: str | None = None,
        content: str | None = None,
        latency: int | None = None,
        memory_bytes: int | None = None,
    ) -> dict | None:
        if id is None and public_id is None:
            raise ValueError("Informe id ou public_id para atualizar.")

        values = {}

        if group is not None:
            values["group"] = group
        if task is not None:
            values["task"] = task
        if status is not None:
            values["status"] = status
        if content is not None:
            values["content"] = content
        if latency is not None:
            values["latency"] = latency
        if memory_bytes is not None:
            values["memory_bytes"] = memory_bytes

        if not values:
            raise ValueError("Informe group, task, status, content, latency ou memory_bytes para atualizar.")

        try:
            async with self.session.begin() as session:
                query = update(ModelObservability).values(**values).returning(ModelObservability)

                if id is not None:
                    query = query.where(ModelObservability.id == id)
                else:
                    if isinstance(public_id, str):
                        public_id = uuid.UUID(public_id)

                    query = query.where(ModelObservability.public_id == public_id)

                result = await session.execute(query)
                data = result.scalar_one_or_none()

                if data is None:
                    return None

                return self._to_dict(data)

        except Exception as error:
            logger.error(text=f"Failed to update observability record: {error}")
            raise

    async def delete(
        self,
        id: int | None = None,
        public_id: uuid.UUID | str | None = None,
    ) -> dict | None:
        if id is None and public_id is None:
            raise ValueError("Informe id ou public_id para deletar.")

        try:
            async with self.session.begin() as session:
                query = delete(ModelObservability).returning(ModelObservability)

                if id is not None:
                    query = query.where(ModelObservability.id == id)
                else:
                    if isinstance(public_id, str):
                        public_id = uuid.UUID(public_id)

                    query = query.where(ModelObservability.public_id == public_id)

                result = await session.execute(query)
                data = result.scalar_one_or_none()

                if data is None:
                    return None

                return self._to_dict(data)

        except Exception as error:
            logger.error(text=f"Failed to delete observability record: {error}")
            raise
