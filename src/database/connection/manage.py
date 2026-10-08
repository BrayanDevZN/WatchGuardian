"junta os modulos"

from .session import create_session
from .engine import Engine

class ConnectionDb(Engine):

    def __init__(self, url:str)-> None:
        super().__init__(url)

        self.engine = self.run()
        self.session = create_session(engine=self.engine)

