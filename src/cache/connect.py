from src.logs.module import Logs
logger = Logs(loglevel="SUCCESS")
import time
"Cria conexão com redis"

from redis import Redis 

class RedisConnect:

    def __init__(self, host:str, port:str|int, password:str|None = None)-> None:

        self.host = host 
        self.port = port 
        self.password = password

    #Cria conexão 
    def _conn(self) -> None:

        try:

            logger.info("Criando conexão com redis...")

            self.client = (Redis(host=self.host, port=self.port, password=self.password, decode_responses=True)
                           if self.password is not None else 
                           Redis(host=self.host, port=self.port, decode_responses=True))

            logger.success("Conexão criada!!")

        except Exception as error:

            logger.error(f"Houve um erro ao criar conexão: {error}")
            raise 

    #testa a conexão
    def _test(self) -> None:

        countdown = 0

        while True:

            try:

                logger.info("Testando conexão com redis...")

                self.client.ping()

                logger.success("Conexão ok!!")

                break 

            except Exception as error:

                if countdown !=3:

                    logger.warning("Houve um erro na conexão, executando um novo teste em 5 segundos...")
                    countdown+=1
                    time.sleep(5)
                    continue 

                logger.error(f"Houve um erro ao se conectar: {error}")
                raise 

    #Executa os metodos e retorna conexão
    def get_client(self) ->Redis:

        self._conn()
        self._test()
        return self.client
    

                
        
