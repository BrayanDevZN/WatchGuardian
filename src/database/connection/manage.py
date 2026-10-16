"junta os modulos"

from .session import create_session
from .engine import Engine
import asyncio
class ConnectionDb(Engine):

    def __init__(self, url:str)-> None:
        super().__init__(url)
        self.url = url

    async def run(self) -> None:

        self.engine = await self.get_engine()
        self.session = create_session(engine=self.engine)

        
        
