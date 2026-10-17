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
        self.logs.info("Inicializando ProjectSettings.")

        self.settings = Settings(env_file=env_file)
        self.local = local

        self.logs.info(
            f"ProjectSettings inicializado (env_file={'definido' if env_file else 'padrão'}, "
            f"local={self.local})."
        )

    def local_secret(self) -> None:
        """Adiciona secrets consumidas pelos módulos públicos."""
        defaults = {
            # CacheManage, WatchDb e Replicators
            "host": "localhost",
            "port": "6379",
            "password": None,
            # WatchServer e middleware de rate limit
            "origin": "*",
            "rate_limit": "100",
            # WatchAuth
            "secret": token_urlsafe(32),
            # ClientHttp e WatchDb(http=True)
            "url": "http://localhost:8000",
            "token": None,
            # WatchDb(http=False)
            "url_db": None,
        }

        self.logs.info("Iniciando configuração local de secrets.")
        self.settings.add_secret(list(defaults))

        for name, default in defaults.items():
            value = self.settings.get_secret(name)
            if value is None or value == "":
                self.settings.secrets[name] = default
                source = "default local"
            else:
                source = "ambiente/.env"

            # Registra o nome e a origem, nunca o conteúdo de uma secret.
            self.logs.info(f"Secret '{name}' configurada ({source}).")

        self.logs.success("Configuração local de secrets concluída.")

    def local_config(self) -> None:
        """Adiciona configs consumidas pelo banco e pelo balanceador."""
        defaults = {
            # WatchDb local
            "path": None,
            # Replicators / WatchBalance
            "replicator_name": "watchguardian-local",
            "replicator_urls": ["http://localhost:8000"],
            "replicator_paths": "*",
            "replicator_methods": "*",
            "replicator_limit": 60,
            "replicator_expires": 60,
        }

        self.logs.info("Iniciando configuração local de configs.")

        for name, value in defaults.items():
            if name not in self.settings.configs:
                self.settings.add_config({"name": name, "value": value})
                source = "default local"
            else:
                source = "valor existente"

            self.logs.info(f"Config '{name}' registrada ({source}).")

        self.logs.success("Configuração local de configs concluída.")

    def get(self) -> Settings:
        """Retorna Settings; aplica defaults quando local=True."""
        self.logs.info("Preparando Settings do projeto.")

        if self.local:
            self.logs.info("Modo local habilitado.")
            self.local_secret()
            self.local_config()
        else:
            self.logs.info("Modo local desabilitado; defaults locais não serão aplicados.")

        self.logs.success("Settings do projeto pronto para uso.")
        return self.settings
