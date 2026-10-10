"""
Controla a tabela de logs com cache-aside opcional.
"""

import json
import uuid
from typing import Any

from src.cache.manage import RedisManage as CacheManage
from src.database.manage import ControlDb


class LogsService:

    def __init__(self, control_db: ControlDb, cache: CacheManage | None = None) -> None:
        self.control_db = control_db
        self.cache = cache
        self.db = control_db.logs

    @staticmethod
    def _serialize(data: Any) -> dict:
        return {
            "data": json.dumps(data, default=str)
        }

    @staticmethod
    def _deserialize(data: dict | None) -> Any:
        if not data or "data" not in data:
            return None
        return json.loads(data["data"])

    @staticmethod
    def _key(id: int | None = None, public_id: uuid.UUID | str | None = None) -> str:
        if id is not None:
            return f"watchguardian:logs:id:{id}"
        if public_id is not None:
            return f"watchguardian:logs:public_id:{public_id}"
        return "watchguardian:logs:all"

    async def _save_cache(self, key: str, data: Any) -> None:
        if self.cache is not None and data is not None:
            await self.cache.hash(key=key, data=self._serialize(data))

    async def _delete_cache(
        self,
        id: int | None = None,
        public_id: uuid.UUID | str | None = None,
    ) -> None:
        if self.cache is None:
            return

        await self.cache.delete("watchguardian:logs:all")

        if id is not None:
            await self.cache.delete(self._key(id=id))

        if public_id is not None:
            await self.cache.delete(self._key(public_id=public_id))

    async def create(self, log: str, status: str) -> dict:
        data = await self.db.create(log=log, status=status)

        if self.cache is not None:
            await self.cache.delete("watchguardian:logs:all")
            await self._save_cache(self._key(id=data["id"]), data)
            await self._save_cache(self._key(public_id=data["public_id"]), data)

        return data

    async def select(
        self,
        id: int | None = None,
        public_id: uuid.UUID | str | None = None,
    ) -> dict | list[dict] | None:
        key = self._key(id=id, public_id=public_id)

        if self.cache is not None:
            cached = await self.cache.read(key=key, hash=True)
            cached_data = self._deserialize(cached)

            if cached_data is not None:
                return cached_data

        data = await self.db.select(id=id, public_id=public_id)

        if self.cache is not None and data is not None:
            await self._save_cache(key, data)

        return data

    async def update(
        self,
        id: int | None = None,
        public_id: uuid.UUID | str | None = None,
        log: str | None = None,
        status: str | None = None,
    ) -> dict | None:
        data = await self.db.update(
            id=id,
            public_id=public_id,
            log=log,
            status=status,
        )

        if data is not None:
            await self._delete_cache(
                id=data.get("id", id),
                public_id=data.get("public_id", public_id),
            )

        return data

    async def delete(
        self,
        id: int | None = None,
        public_id: uuid.UUID | str | None = None,
    ) -> dict | None:
        data = await self.db.delete(id=id, public_id=public_id)

        if data is not None:
            await self._delete_cache(
                id=data.get("id", id),
                public_id=data.get("public_id", public_id),
            )

        return data
