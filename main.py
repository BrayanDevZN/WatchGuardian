from src.server.manage import Server
from src.service.module import Settings

settings = Settings(env_file=".env")

settings.add_secret(
    [
        "secret",
        "origin",
        "port",
        "rate_limit",
        "host"
    ]
)

instance = Server(settings=settings)
app = instance.run()