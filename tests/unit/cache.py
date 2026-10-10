"""
Teste de CacheManage
"""

import asyncio
import os

from src.service.module import CacheManage, Settings


async def test_cache() -> None:

    os.environ["host"] = "localhost"
    os.environ["port"] = "6379"

    print("\n=== SETTINGS ===")

    settings = Settings()

    settings.add_secret([
        "host",
        "port",
        "password"
    ])

    print("\n=== CREATE CACHE ===")

    cache = CacheManage(
        settings=settings
    )

    print("\n=== CLEAN OLD DATA ===")

    await cache.delete("test:counter")
    await cache.delete("test:user")
    await cache.delete("test:delete")
    await cache.delete("test:expire")

    print("\n=== INCR ===")

    result = await cache.incr("test:counter")
    print(result)

    result = await cache.incr("test:counter")
    print(result)

    print("\n=== READ ===")

    result = await cache.read("test:counter")
    print(result)

    print("\n=== HASH ===")

    await cache.hash(
        key="test:user",
        data={
            "name": "Brayan",
            "framework": "WatchGuardian",
            "status": "active"
        }
    )

    print("\n=== READ HASH ===")

    result = await cache.read(
        key="test:user",
        hash=True
    )

    print(result)

    print("\n=== DELETE ===")

    await cache.hash(
        key="test:delete",
        data={
            "value": "delete-me"
        }
    )

    result = await cache.delete("test:delete")
    print(result)

    print("\n=== READ AFTER DELETE ===")

    result = await cache.read("test:delete")
    print(result)

    print("\n=== PUBLISH / LISTEN ===")

    async def publish_event() -> None:
        await asyncio.sleep(0.5)

        result = await cache.publish(
            channel="test:events",
            event="watchguardian_event"
        )

        print(
            "Quantidade de listeners:",
            result
        )

    publish_task = asyncio.create_task(
        publish_event()
    )

    async for event in cache.listen("test:events"):
        print(
            "Evento recebido:",
            event
        )

        break

    await publish_task

    print("\n=== CUSTOM EXPIRE ===")

    await cache.incr(
        key="test:expire",
        time=10
    )

    result = await cache.read("test:expire")
    print(result)

    print("\n=== CLEAN FINAL ===")

    await cache.delete("test:counter")
    await cache.delete("test:user")
    await cache.delete("test:expire")

    print("\n=== TESTE FINALIZADO ===")


if __name__ == "__main__":
    asyncio.run(test_cache())