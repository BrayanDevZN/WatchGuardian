"junta os modulos de redis"


from .connect import RedisConnect
from .control import RedisControl

class RedisManage(RedisControl):
    def __init__(self, host:str, port:int|str, password = None):
        client = RedisConnect(host=host, port=port, password=password).get_client()

        super().__init__(client=client)