"teste de replicate"

from WatchGuardian._internal.replicator.module import Replicator, Replicators
from WatchGuardian._internal.service.module import CacheManage, Settings
import asyncio
import os


async def test_replicate() -> None:
    url = "http://localhost:800"

    os.environ["port"] = "6379"
    os.environ["host"] = "localhost"

    settings = Settings()

    settings.add_secret(secrets="port")
    settings.add_secret(secrets="host")

    settings.add_config(configs=[
        {"name": "replicator_name", "value": "teste"},
        {"name": "replicator_urls", "value": [url + str(n) for n in range(3)]},
        {"name": "replicator_paths", "value": "*"},
        {"name": "replicator_methods", "value": "*"},
        {"name": "replicator_limit", "value": 30},
        {"name": "replicator_expires", "value": 60}
    ])

    cache = CacheManage(settings=settings)

    instance = Replicator(url=url + "0", cache=cache, paths="*", methods="*", name="teste", limit=60, limit_expires=30)

    print(await instance.valid())

    instance = Replicators(settings=settings)
    replicas = await instance.get_replicas()

    for replica in replicas:
        print(await replica.valid())


if __name__ == "__main__":
    asyncio.run(test_replicate())