"""Configuração pronta para iniciar um projeto WatchGuardian."""

from secrets import token_urlsafe

from src.service.module import Settings, WatchLogs


class ProjectSettings:
    """Cria e retorna Settings com defaults locais opcionais."""

    def __init__(
        self,
        env_file: str | None = None,
        local: bool = False,
    ) -> None:
        self.settings = Settings(env_file=env_file)
        self.local = local
        self.logs = WatchLogs()

    def local_secret(self) -> None:
        """Registra secrets usadas pelos módulos com defaults de desenvolvimento."""
        defaults = {
            "host": "localhost",
            "port": "6379",
            "password": None,
            "secret": token_urlsafe(32),
            "origin": "*",
            "rate_limit": "100",
            "url": "http://localhost:8000",
            "url_db": None,
            "token": None,
        }

        # Lê valores do ambiente/.env. Os defaults abaixo só preenchem
        # secrets ausentes; valores definidos pelo usuário têm prioridade.
        self.settings.add_secret(list(defaults))

        for name, default in defaults.items():
            value = self.settings.get_secret(name)
            if value is None or value == "":
                self.settings.secrets[name] = default

        self.logs.info("Secrets locais adicionadas ao Settings.")

    def local_config(self) -> None:
        """Registra configs locais usadas pelo banco e pelo replicator."""
        defaults = {
            "path": None,
            "replicator_name": "watchguardian-local",
            "replicator_urls": ["http://localhost:8000"],
            "replicator_paths": "*",
            "replicator_methods": "*",
            "replicator_limit": 60,
            "replicator_expires": 60,
        }

        for name, value in defaults.items():
            if name not in self.settings.configs:
                self.settings.add_config({"name": name, "value": value})

        self.logs.info("Configs locais adicionadas ao Settings.")

    def get(self) -> Settings:
        """Retorna Settings, adicionando defaults se local=True."""
        if self.local:
            self.local_secret()
            self.local_config()

        return self.settings
