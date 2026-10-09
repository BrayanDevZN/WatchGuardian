"""
junta os modulos
"""

from .context import ControlDb, WatchLogs, ObsContext, ObsControl


class WatchObs(ObsControl):
    def __init__(self, logs:WatchLogs, control_db:ControlDb)-> None:
        super().__init__(logs, control_db)
        


    #metodo que retorna o gerenciador de contexto
    def begin(self, name:str) -> ObsContext:

        return ObsContext(
            name=name,
            control_db=self.control_db,
            logs=self.logs
        )

