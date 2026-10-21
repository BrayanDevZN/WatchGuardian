"""Load generated WatchGuardian projects for CLI commands."""

import importlib.util
import inspect
import sys
from pathlib import Path
from types import ModuleType


def resolve_project_path(project_path: str | Path | None) -> Path | None:
    """Resolve an explicit project or the default ./watchguardian project."""
    if project_path is None:
        candidate = (Path.cwd() / "watchguardian").resolve()
        if not candidate.is_dir():
            return None
        project_path = candidate

    directory = Path(project_path).expanduser().resolve()
    if not directory.exists() or not directory.is_dir():
        raise FileNotFoundError(f"Project directory does not exist: {directory}")

    main_file = directory / "main.py"
    settings_file = directory / "settings.json"
    if not main_file.is_file():
        raise FileNotFoundError(f"Project entry point was not found: {main_file}")
    if not settings_file.is_file():
        raise FileNotFoundError(f"Project settings file was not found: {settings_file}")
    return directory


def add_project_argument(parser, *, default=None) -> None:
    """Add the optional generated-project directory argument."""
    parser.add_argument(
        "--project",
        type=Path,
        default=default,
        help="Generated project directory (defaults to ./watchguardian when present)",
    )


def load_project_app(project_path: str | Path | None):
    """Import and return the generated project's app without loading modules."""
    directory = resolve_project_path(project_path)
    if directory is None:
        return None

    main_file = directory / "main.py"
    package_name = f"watchguardian_project_{abs(hash(directory))}"
    package = ModuleType(package_name)
    package.__path__ = [str(directory)]
    package.__package__ = package_name
    sys.modules[package_name] = package

    project_directory = str(directory)
    if project_directory in sys.path:
        sys.path.remove(project_directory)
    sys.path.insert(0, project_directory)

    module_name = f"{package_name}.main"
    spec = importlib.util.spec_from_file_location(module_name, main_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not import project entry point: {main_file}")

    project_module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = project_module
    spec.loader.exec_module(project_module)

    app = getattr(project_module, "app", None)
    if app is None or not callable(getattr(app, "load_module", None)):
        raise AttributeError(
            f"Project entry point must define app with an async load_module(): {main_file}"
        )
    return app


def load_project_settings(app):
    """Build project Settings without starting logging, server, or balance modules."""
    load_settings = getattr(app, "load_settings", None)
    if callable(load_settings):
        return load_settings()

    # Compatibility for projects generated before ProjectApp.load_settings existed.
    from WatchGuardian.project.watchguardian.settings import (
        ProjectSettings,
        resolve_project_configs,
    )

    env_file = app.project_config.get("env_file")
    if env_file is not None:
        env_path = Path(env_file)
        if not env_path.is_absolute():
            env_file = str(app.settings_path.parent / env_path)

    app.local = env_file is None
    app.http = None if app.local else True
    settings = ProjectSettings(env_file=env_file, local=True).get()

    configs = resolve_project_configs(
        project_root=app.settings_path.parent,
        configs=app.project_config.get("configs", {}),
    )
    for name, value in configs.items():
        settings.add_config({"name": name, "value": value})

    app.settings = settings
    return settings


async def load_project_modules(
    project_path: str | Path | None,
    modules: tuple[str, ...] | list[str],
):
    """Load only requested modules from a generated project."""
    app = load_project_app(project_path)
    if app is None:
        return None

    settings = load_project_settings(app)
    project_main = sys.modules.get(type(app).__module__)
    module_class = getattr(project_main, "WatchModule", None)
    if module_class is None:
        from WatchGuardian.project.watchguardian.module import WatchModule as module_class

    module = module_class(
        settings=settings,
        http=app.http,
        loglevel=app.project_config.get("loglevel", "INFO"),
    )
    app.module = module

    initializers = {
        "database": module.database,
        "logs": module.logs,
        "observability": module.observability,
        "auth": module.auth,
        "cache": module.cache_module,
        "client": module.client,
        "server": module.server,
        "replicators": getattr(module, "replica_module", None),
        "balance": module.balance,
    }

    for name in modules:
        try:
            initializer = initializers[name]
        except KeyError:
            available = ", ".join(sorted(initializers))
            raise ValueError(
                f"Unknown project module {name!r}. Available modules: {available}"
            ) from None

        if name == "replicators" and initializer is None:
            # Older generated templates did not expose replica_module().
            from WatchGuardian._internal.service.module import Replicators

            module.replicators = Replicators(settings=settings)
            continue

        initialized = initializer()
        if inspect.isawaitable(initialized):
            await initialized

    return module


async def load_project(project_path: str | Path | None):
    """Import app from a project directory and return its fully loaded WatchModule."""
    app = load_project_app(project_path)
    if app is None:
        return None
    return await app.load_module()
