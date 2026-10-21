"""Configuração funcional do balanceador para o CI."""

from WatchGuardian._internal.service.module import CacheManage, Replicator, Settings, WatchBalance


settings = Settings()
settings.secrets.update(
    {
        "host": "127.0.0.1",
        "port": "6379",
        "password": None,
    }
)

cache = CacheManage(settings=settings)
replicas = [
    Replicator(
        url=f"http://127.0.0.1:{port}",
        cache=cache,
        name=f"functional_api_{port}",
        paths="*",
        methods=["GET"],
        limit=100,
        limit_expires=60,
    )
    for port in (8000, 8001, 8002)
]

app = WatchBalance(replicas=replicas).run()
