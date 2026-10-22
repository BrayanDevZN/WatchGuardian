"""Generated project entry point."""

import asyncio
import json
from pathlib import Path
from dotenv import dotenv_values

if __package__:
    from .module import WatchModule
    from .settings import DEFAULT_CONFIGS, ProjectSettings, resolve_project_configs
else:
    from src.project.watchguardian.module import WatchModule
    from src.project.watchguardian.settings import (
        DEFAULT_CONFIGS,
        ProjectSettings,
        resolve_project_configs,
    )


class ProjectApp:
    """Load project settings and expose all initialized WatchGuardian modules."""

    def __init__(self) -> None:
        self.settings_path = Path(__file__).with_name("settings.json")
        with self.settings_path.open(encoding="utf-8") as settings_file:
            self.project_config = json.load(settings_file)
        self.name = self.project_config.get("name", "watchguardian")
        self.local = self.project_config.get("local", True)
        self.http = self.project_config.get("http")
        self.settings = None
        self.module: WatchModule | None = None

    def _loaded_module(self) -> WatchModule:
        if self.module is None:
            raise RuntimeError(
                "Project modules are not loaded yet; call "
                "'await app.load_module()' before accessing them."
            )
        return self.module

    @property
    def watch_db(self):
        return self._loaded_module().watch_db

    @property
    def watch_logs(self):
        return self._loaded_module().watch_logs

    @property
    def watch_obs(self):
        return self._loaded_module().watch_obs

    @property
    def watch_auth(self):
        return self._loaded_module().watch_auth

    @property
    def cache(self):
        return self._loaded_module().cache

    @property
    def client_http(self):
        return self._loaded_module().client_http

    @property
    def watch_server(self):
        return self._loaded_module().watch_server

    @property
    def server_app(self):
        return self._loaded_module().server_app

    @property
    def replicators(self):
        return self._loaded_module().replicators

    @property
    def watch_balance(self):
        return self._loaded_module().watch_balance

    @property
    def balance_app(self):
        return self._loaded_module().balance_app

    def __getattr__(self, name: str):
        """Forward other module attributes for backward compatibility."""
        module = self.__dict__.get("module")
        if module is None:
            raise AttributeError(
                f"Project modules are not loaded yet; call "
                f"'await app.load_module()' before accessing '{name}'."
            )
        try:
            return getattr(module, name)
        except AttributeError:
            raise AttributeError(
                f"{type(self).__name__!s} has no attribute {name!r}; "
                "check the available WatchModule attributes."
            ) from None

    def load_settings(self):
        """Load the project's .env and settings.json with local fallbacks."""
        if self.settings is not None:
            return self.settings

        env_file = self.project_config.get("env_file")
        if env_file is not None:
            env_path = Path(env_file)
            if not env_path.is_absolute():
                env_file = str((self.settings_path.parent / env_path).resolve())

        self.local = self.project_config.get("local", env_file is None)
        self.http = self.project_config.get(
            "http", None if self.local else True
        )

        project_settings = ProjectSettings(env_file=env_file, local=self.local)
        self.settings = project_settings.get()

        config_values = dict(DEFAULT_CONFIGS)
        config_values.update(self.project_config.get("configs", {}))
        if env_file is not None:
            for name, raw_value in dotenv_values(env_file).items():
                if name in config_values and raw_value not in (None, ""):
                    try:
                        config_values[name] = json.loads(raw_value)
                    except json.JSONDecodeError:
                        config_values[name] = raw_value

        configs = resolve_project_configs(
            project_root=self.settings_path.parent,
            configs=config_values,
        )
        self.settings.configs.clear()
        for name, value in configs.items():
            self.settings.add_config({"name": name, "value": value})
        return self.settings

    async def load_module(self) -> WatchModule:
        """Apply project settings, initialize modules, and return WatchModule."""
        self.module = WatchModule(
            settings=self.load_settings(),
            http=self.http,
            loglevel=self.project_config.get("loglevel", "INFO"),
        )
        await self.module.load_modules()
        return self.module


app = ProjectApp()


if __name__ == "__main__":
    asyncio.run(app.load_module())
