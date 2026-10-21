"""Local configuration for projects that use the public WatchGuardian modules."""

import json
import os
from pathlib import Path
from secrets import token_urlsafe

from WatchGuardian._internal.service.module import Settings, WatchLogs


DEFAULT_CONFIGS = {
    "path": "data",
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
    """Prepare settings from an environment file with local defaults as fallback."""

    def __init__(self, env_file: str | None = None, local: bool = False) -> None:
        self.logs = WatchLogs()
        self.logs.info("Initializing ProjectSettings.")
        self.settings = Settings(env_file=env_file)
        self.local = local
        self.logs.info(
            f"ProjectSettings initialized (env_file={'set' if env_file else 'default'}, "
            f"local={self.local})."
        )

    def local_secret(self) -> None:
        """Fill missing secrets with the framework's local defaults."""
        defaults = {
            "host": "localhost",
            "port": "6379",
            "password": None,
            "origin": "*",
            "rate_limit": "100",
            "secret": token_urlsafe(32),
            "url": "http://localhost:8000",
            "token": None,
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
        """Fill missing configs from settings.json or local defaults."""
        self.logs.info("Starting local config setup.")
        for name, default in DEFAULT_CONFIGS.items():
            raw_value = os.getenv(name)
            if raw_value not in (None, ""):
                try:
                    value = json.loads(raw_value)
                except json.JSONDecodeError:
                    value = raw_value
                source = "environment/.env"
            else:
                value = default
                source = "local default"

            if name not in self.settings.configs:
                self.settings.add_config({"name": name, "value": value})
            self.logs.info(f"Config '{name}' registered ({source}).")
        self.logs.success("Local config setup completed.")

    def get(self) -> Settings:
        """Return Settings, applying local defaults to values missing from the environment."""
        self.logs.info("Preparing project Settings.")
        if self.local:
            self.logs.info("Local mode enabled.")
        else:
            self.logs.info("Environment mode enabled with local fallbacks.")
        self.local_secret()
        self.local_config()
        self.logs.success("Project Settings are ready.")
        return self.settings
