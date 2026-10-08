"""
Junta todos os modulos
"""

from .migrate import Migrate
from src.database.connection.manage import ConnectionDb
from src.database.control.observability import ObservabilityDb
from src.database.control.logs import LogsDb

class ControlDb(Migrate):

    def __init__(self, url: str) -> None:

        self.connect = ConnectionDb(url=url)

        self.logs = None
        self.observability = None

    async def run(self) -> None:

        await self.connect.run()

        self.logs = LogsDb(
            session=self.connect.session
        )

        self.observability = ObservabilityDb(
            session=self.connect.session
        )