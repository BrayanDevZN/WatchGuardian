"""
Junta todos os modulos
"""

from .migrate import Migrate
from WatchGuardian._internal.database.connection.manage import ConnectionDb
from WatchGuardian._internal.database.control.observability import ObservabilityDb
from WatchGuardian._internal.database.control.logs import LogsDb

class ControlDb(Migrate):

    def __init__(self, url: str) -> None:

        self.connect = ConnectionDb(url=url)

       

    async def run(self) -> None:

        await self.connect.run()

        super().__init__(engine=self.connect.engine)

        self.logs = LogsDb(
            session=self.connect.session
        )

        self.observability = ObservabilityDb(
            session=self.connect.session
        )