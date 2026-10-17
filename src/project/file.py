"""Copy the WatchGuardian project template to a chosen location."""

import json
import shutil
from pathlib import Path

from WatchGuardian import WatchLogs

from .watchguardian.settings import DEFAULT_CONFIGS


def copy_watchguardian(
    path: str | Path | None = None,
    name: str | None = None,
    env_file: str | Path | None = None,
) -> Path:
    """Copy the complete project template and apply its initial settings.

    If path is omitted, the current working directory is used. If name is
    omitted, the destination folder is named WatchGuardian. The optional
    env_file path is stored in the generated settings.json.
    """
    logger = WatchLogs()
    template = Path(__file__).resolve().parent / "watchguardian"
    destination_root = Path(path) if path is not None else Path.cwd()
    folder_name = "WatchGuardian" if name is None else name

    if (
        not folder_name
        or Path(folder_name).name != folder_name
        or folder_name in {".", ".."}
    ):
        error = ValueError("name must be a non-empty folder name, not a path.")
        logger.error(str(error))
        raise error

    destination = destination_root / folder_name

    logger.info(f"Preparing project template from '{template}'.")

    if not template.is_dir():
        error = FileNotFoundError(f"Project template folder was not found: {template}")
        logger.error(str(error))
        raise error

    if destination.resolve() == template.resolve():
        error = ValueError("The destination cannot be the project template folder.")
        logger.error(str(error))
        raise error

    logger.info(f"Copying project template to '{destination}'.")

    try:
        destination_root.mkdir(parents=True, exist_ok=True)
        shutil.copytree(template, destination)

        settings_path = destination / "settings.json"
        project_settings = json.loads(settings_path.read_text(encoding="utf-8"))
        use_local_settings = env_file is None
        project_settings.update(
            {
                "name": folder_name,
                "path": str(destination.resolve()),
                "env_file": str(env_file) if env_file is not None else None,
                "local": use_local_settings,
                "http": None if use_local_settings else True,
            }
        )
        project_settings.setdefault("configs", DEFAULT_CONFIGS)

        settings_path.write_text(
            json.dumps(project_settings, indent=4) + "\n",
            encoding="utf-8",
        )
    except Exception as error:
        logger.error(f"Failed to create the WatchGuardian project: {error}")
        raise

    logger.success(f"WatchGuardian project created at '{destination}'.")
    return destination
