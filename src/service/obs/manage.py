"""
junta os modulos
"""

from .context import WatchDb, WatchLogs, ObsContext, ObsControl


class WatchObs(ObsControl):
    def __init__(self, logs:WatchLogs, watch_db=WatchDb)-> None:
        super().__init__(logs, watch_db)
        


    #metodo que retorna o gerenciador de contexto
    def begin(self, name:str) -> ObsContext:

        return ObsContext(
            name=name,
            watch_db=self.control_db,
            logs=self.logs
        )

