"""Local configuration for projects that use the public WatchGuardian modules."""

from pathlib import Path
from secrets import token_urlsafe

from src.service.module import Settings, WatchLogs


DEFAULT_CONFIGS = {
    # Local WatchDb
    "path": "data",
    # Replicators / WatchBalance
    "replicator_name": "watchguardian-local",
    "replicator_urls": ["http://localhost:8000"],
    "replicator_paths": "*",
    "replicator_methods": "*",
    "replicator_limit": 60,
    "replicator_expires": 60,
}


def resolve_project_configs(
    project_root: str | Path,
    configs: dict[str, object],
) -> dict[str, object]:
    """Resolve project-relative SQLite paths from the generated project root."""
    resolved_configs = dict(configs)
    configured_path = resolved_configs.get("path") or "data"
    database_directory = Path(configured_path).expanduser()
    if not database_directory.is_absolute():
        database_directory = Path(project_root).expanduser() / database_directory
    database_directory = database_directory.resolve()
    database_directory.mkdir(parents=True, exist_ok=True)
    resolved_configs["path"] = str(database_directory)
    return resolved_configs


class ProjectSettings:
    """Prepare settings used by the public WatchGuardian modules."""

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
        """Add secrets consumed by the public modules."""
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

            self.logs.info(f"Secret '{name}' configured ({source}).")

        self.logs.success("Local secrets setup completed.")

    def local_config(self) -> None:
        """Add configs consumed by WatchDb and the load balancer."""
        self.logs.info("Starting local config setup.")

        for name, value in DEFAULT_CONFIGS.items():
            if name not in self.settings.configs:
                self.settings.add_config({"name": name, "value": value})
                source = "local default"
            else:
                source = "existing value"

            self.logs.info(f"Config '{name}' registered ({source}).")

        self.logs.success("Local config setup completed.")

    def get(self) -> Settings:
        """Return Settings, applying local defaults when local=True."""
        self.logs.info("Preparing project Settings.")

        if self.local:
            self.logs.info("Local mode enabled.")
            self.local_secret()
            self.local_config()
        else:
            self.logs.info("Local mode disabled; local defaults will not be applied.")

        self.logs.success("Project Settings are ready.")
        return self.settings
