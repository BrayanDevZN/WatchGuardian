"""Copy the public WatchGuardian package into a project directory."""

import shutil
from pathlib import Path

from WatchGuardian import WatchLogs


def copy_watchguardian(
    path: str | Path | None = None,
    name: str | None = None,
) -> Path:
    """Copy WatchGuardian into path and return the destination.

    If path is omitted, the current working directory is used. If name is
    omitted, the copied folder keeps the default name, WatchGuardian.
    """
    logger = WatchLogs()
    source = Path(__file__).resolve().parents[3] / "WatchGuardian"
    destination_root = Path(path) if path is not None else Path.cwd()
    folder_name = name or "WatchGuardian"

    if Path(folder_name).name != folder_name or folder_name in {".", ".."}:
        raise ValueError("name must be a folder name, not a path.")

    destination = destination_root / folder_name

    logger.info(f"Preparing to copy WatchGuardian from '{source}'.")

    if not source.is_dir():
        error = FileNotFoundError(f"WatchGuardian source folder was not found: {source}")
        logger.error(str(error))
        raise error

    if destination.resolve() == source.resolve():
        error = ValueError("The destination cannot be the WatchGuardian source folder.")
        logger.error(str(error))
        raise error

    destination_root.mkdir(parents=True, exist_ok=True)
    logger.info(f"Copying WatchGuardian to '{destination}'.")

    try:
        shutil.copytree(source, destination)
    except Exception as error:
        logger.error(f"Failed to copy WatchGuardian: {error}")
        raise

    logger.success(f"WatchGuardian copied to '{destination}'.")
    return destination
