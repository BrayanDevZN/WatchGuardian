"""
junta obs com db
"""

from src.service.logs import WatchLogs, WatchDb
import time 
import uuid

class ObsControl:

    def __init__(self,logs:WatchLogs, watch_db:WatchDb)->None:

        self.logs = logs 
        self.control_db = watch_db
        

    async def task(self, name:str) -> uuid.UUID:

        self.name = name 
        self.start = time.perf_counter()
        self.id = uuid.uuid4()

        
        await self.control_db.observability.create(
            status="pending",
            task=name,
            content="init",
            latency=0,
            public_id=self.id
        )

        self.logs.info(f"task {name} iniciada!")

        return self.id

    async def commit(self, content:str, error:bool=False) -> None:
        end = time.perf_counter()
        latency = end - self.start

        await self.control_db.observability.update(
            public_id=self.id,
            content=content,
            status="sucess" if not error else "failure", 
            latency=latency           
        )

        if error:

            self.logs.error(f"Houve um erro na task {self.name}: {content}")

        else:

            self.logs.success(f"task {self.name} executada com sucesso!!")

    async def close(self) -> None:

        await self.control_db.observability.delete(public_id=self.id)
        self.logs.success(f"task {self.name} encerrada!")

   




        



   
        




        
