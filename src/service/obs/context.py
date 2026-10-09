"""
Classe que gerencia o contexto
"""

from .watch import ObsControl, ControlDb, WatchLogs
import traceback
class ObsContext(ObsControl):

    def __init__(self, logs:WatchLogs, control_db:ControlDb, name:str):

        super().__init__(logs, control_db)
        self.name = name


    async def __aenter__(self)-> ObsContext:

        await self.task(name=self.name)

        return self 

    async def __aexit__(self, exc_type, exc, tb)-> bool:

        content = (
            "".join(
                traceback.format_exception(
                    exc_type,
                    exc,
                    tb
                )
            ) if exc_type is not None else "executed"
        )

        await self.commit(content=content if exc_type is None else tb, error=True if exc_type is not None else False)

        return False

       








        

    

        


        