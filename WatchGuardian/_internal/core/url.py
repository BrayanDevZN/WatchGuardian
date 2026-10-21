"""Database URL helpers."""

from pathlib import Path

from sqlalchemy.engine import URL


def config_url(url: str | None = None, path: str | None = None) -> str:
    """Return a configured database URL or a project-local SQLite URL.

    ``path`` is the directory that will contain ``watch.db``. It is created
    when missing, so a fresh project can start without a separate migration
    setup step.
    """
    if url and url.strip():
        return url.strip()

    database_directory = Path(path or "data").expanduser().resolve()
    database_directory.mkdir(parents=True, exist_ok=True)
    database_file = database_directory / "watch.db"

    return URL.create(
        drivername="sqlite+aiosqlite",
        database=str(database_file),
    ).render_as_string(hide_password=False)
