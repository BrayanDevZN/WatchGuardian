"""Inicializa e retorna o agregador de módulos de um projeto."""

from src.file.project.module import WatchModule
from src.file.project.settings import ProjectSettings


async def watch_manage(
    env_file: str | None = None,
    local: bool = True,
    http: bool = False,
    loglevel: str = "INFO",
) -> WatchModule:
    """Cria Settings, carrega todos os módulos e retorna WatchModule."""
    project_settings = ProjectSettings(
        env_file=env_file,
        local=local,
    )
    settings = project_settings.get()

    modules = WatchModule(
        settings=settings,
        http=http,
        loglevel=loglevel,
    )
    await modules.load_modules()

    return modules
