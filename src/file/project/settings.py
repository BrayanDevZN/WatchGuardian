"""Configuração local para projetos que usam os módulos públicos WatchGuardian."""

from secrets import token_urlsafe

from WatchGuardian import Settings, WatchLogs


class ProjectSettings:
    """Prepara as variáveis dos módulos públicos do WatchGuardian."""

    def __init__(
        self,
        env_file: str | None = None,
        local: bool = False,
    ) -> None:
        self.logs = WatchLogs()
        self.logs.info("Initializing ProjectSettings.")

        self.settings = Settings(env_file=env_file)
        self.local = local

        self.logs.info(
            f"ProjectSettings initialized (env_file={'set' if env_file else 'default'}, "
            f"local={self.local})."
        )

    def local_secret(self) -> None:
        """Adiciona secrets consumidas pelos módulos públicos."""
        defaults = {
            # CacheManage, WatchDb and Replicators
            "host": "localhost",
            "port": "6379",
            "password": None,
            # WatchServer and rate limit middleware
            "origin": "*",
            "rate_limit": "100",
            # WatchAuth
            "secret": token_urlsafe(32),
            # ClientHttp and WatchDb(http=True)
            "url": "http://localhost:8000",
            "token": None,
            # WatchDb(http=False)
            "url_db": None,
        }

        self.logs.info("Starting local secrets setup.")
        self.settings.add_secret(list(defaults))

        for name, default in defaults.items():
            value = self.settings.get_secret(name)
            if value is None or value == "":
                self.settings.secrets[name] = default
                source = "local default"
            else:
                source = "environment/.env"

            # Log the variable name and source, never the secret value.
            self.logs.info(f"Secret '{name}' configured ({source}).")

        self.logs.success("Local secrets setup completed.")

    def local_config(self) -> None:
        """Adiciona configs consumidas pelo banco e pelo balanceador."""
        defaults = {
            # Local WatchDb
            "path": None,
            # Replicators / WatchBalance
            "replicator_name": "watchguardian-local",
            "replicator_urls": ["http://localhost:8000"],
            "replicator_paths": "*",
            "replicator_methods": "*",
            "replicator_limit": 60,
            "replicator_expires": 60,
        }

        self.logs.info("Starting local config setup.")

        for name, value in defaults.items():
            if name not in self.settings.configs:
                self.settings.add_config({"name": name, "value": value})
                source = "local default"
            else:
                source = "existing value"

            self.logs.info(f"Config '{name}' registered ({source}).")

        self.logs.success("Local config setup completed.")

    def get(self) -> Settings:
        """Retorna Settings; aplica defaults quando local=True."""
        self.logs.info("Preparing project Settings.")

        if self.local:
            self.logs.info("Local mode enabled.")
            self.local_secret()
            self.local_config()
        else:
            self.logs.info("Local mode disabled; local defaults will not be applied.")

        self.logs.success("Project Settings are ready.")
        return self.settings
