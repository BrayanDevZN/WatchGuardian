"""Configuração local da API do WatchGuardian para testes funcionais."""

from src.service.module import Settings, WatchServer


ENV_FILE = ".env"

settings = Settings(env_file=ENV_FILE)

settings.add_secret(
    [
        "secret",
        "origin",
        "host",
        "port",
        "password",
        "rate_limit",
        "url_db",
    ]
)

server = WatchServer(settings=settings)
app = server.run()
