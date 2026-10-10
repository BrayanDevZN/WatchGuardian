"""Configuração local da API do WatchGuardian para testes funcionais."""

from src.service.module import Settings, WatchServer


TEST_SECRET = "watchguardian-functional-test-secret-2026"

settings = Settings()

settings.secrets.update(
    {
        "secret": TEST_SECRET,
        "origin": "*",
        "host": "127.0.0.1",
        "port": "6379",
        "password": None,
        "rate_limit": "1000",
        "url_db": None,
    }
)

server = WatchServer(settings=settings)
app = server.run()
