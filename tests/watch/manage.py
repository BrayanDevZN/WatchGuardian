"""Initialize and return the project module aggregator."""

from .module import WatchModule
from .settings import ProjectSettings


async def watch_manage(
    env_file: str | None = None,
    loglevel: str = "INFO",
) -> WatchModule:
    """Use local defaults without env_file; use HTTP mode when one is provided."""
    use_local_settings = env_file is None
    http = None if use_local_settings else True

    project_settings = ProjectSettings(
        env_file=env_file,
        local=use_local_settings,
    )
    settings = project_settings.get()

    modules = WatchModule(
        settings=settings,
        http=http,
        loglevel=loglevel,
    )
    await modules.load_modules()

    return modules
