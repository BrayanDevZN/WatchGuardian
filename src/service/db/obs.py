"""
Controla observabilidade com cache-aside opcional usando banco local ou cliente HTTP.
"""

import json
import uuid
from typing import Any

from src.database.manage import ControlDb
from src.service.cache import CacheManage
from src.service.client import ClientHttp


class ObsService:

    def __init__(
        self,
        control: ControlDb | ClientHttp,
        cache: CacheManage | None = None,
    ) -> None:
        self.control = control
        self.cache = cache
        self.http = isinstance(control, ClientHttp)

        if self.http:
            token = control.settings.required_secrets("token")
            self.db = control.obs(token=token)
        else:
            self.db = control.observability

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
            return f"watchguardian:observability:id:{id}"
        if public_id is not None:
            return f"watchguardian:observability:public_id:{public_id}"
        return "watchguardian:observability:all"

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

        await self.cache.delete("watchguardian:observability:all")

        if id is not None:
            await self.cache.delete(self._key(id=id))

        if public_id is not None:
            await self.cache.delete(self._key(public_id=public_id))

    async def create(
        self,
        task: str,
        status: str,
        content: str,
        latency: int | float,
        public_id: uuid.UUID | None = None,
    ) -> dict:
        if self.http:
            data = await self.db.create_obs(
                task=task,
                status=status,
                content=content,
                latency=latency,
            )
        else:
            data = await self.db.create(
                task=task,
                status=status,
                content=content,
                latency=latency,
                public_id=public_id,
            )

        if self.cache is not None and data is not None:
            await self.cache.delete("watchguardian:observability:all")
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

        if self.http:
            data = await self.db.get_obs(id=id, public_id=public_id)
        else:
            data = await self.db.select(id=id, public_id=public_id)

        if self.cache is not None and data is not None:
            await self._save_cache(key, data)

        return data

    async def update(
        self,
        id: int | None = None,
        public_id: uuid.UUID | str | None = None,
        task: str | None = None,
        status: str | None = None,
        content: str | None = None,
        latency: int | float | None = None,
    ) -> dict | None:
        if self.http:
            data = await self.db.update_obs(
                id=id,
                public_id=public_id,
                task=task,
                status=status,
                content=content,
                latency=latency,
            )
        else:
            data = await self.db.update(
                id=id,
                public_id=public_id,
                task=task,
                status=status,
                content=content,
                latency=latency,
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
        if self.http:
            data = await self.db.delete_obs(id=id, public_id=public_id)
        else:
            data = await self.db.delete(id=id, public_id=public_id)

        if data is not None:
            await self._delete_cache(
                id=data.get("id", id),
                public_id=data.get("public_id", public_id),
            )

        return data
