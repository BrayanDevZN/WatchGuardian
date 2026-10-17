"""Inicializa e retorna o agregador de módulos de um projeto."""

from src.file.project.module import WatchModule
from src.file.project.settings import ProjectSettings


async def watch_manage(
    env_file: str | None = None,
    loglevel: str = "INFO",
) -> WatchModule:
    """Usa defaults locais sem env_file; com arquivo, conecta ao WatchGuardian HTTP."""
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
