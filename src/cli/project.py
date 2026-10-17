"""Load a generated WatchGuardian project for CLI commands."""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def add_project_argument(parser) -> None:
    """Add the optional generated-project directory argument."""
    parser.add_argument(
        "--project",
        type=Path,
        default=None,
        help="Generated project directory containing main.py and settings.json",
    )


async def load_project(project_path: str | Path | None):
    """Import app from a project directory and return its loaded WatchModule."""
    if project_path is None:
        return None

    directory = Path(project_path).expanduser().resolve()
    if not directory.exists() or not directory.is_dir():
        raise FileNotFoundError(f"Project directory does not exist: {directory}")

    main_file = directory / "main.py"
    settings_file = directory / "settings.json"
    if not main_file.is_file():
        raise FileNotFoundError(f"Project entry point was not found: {main_file}")
    if not settings_file.is_file():
        raise FileNotFoundError(f"Project settings file was not found: {settings_file}")

    module_name = f"watchguardian_project_{abs(hash(directory))}"
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

    return await app.load_module()
