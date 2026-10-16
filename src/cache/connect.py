from src.logs.module import Logs
logger = Logs(loglevel="SUCCESS")
import time
"Cria conexão com redis"

from redis import Redis


class RedisConnect:

    def __init__(self, host: str, port: str | int, password: str | None = None) -> None:
        self.host = host
        self.port = port
        self.password = password

    def _conn(self) -> None:
        try:
            logger.info("Creating Redis connection...")

            self.client = (
                Redis(host=self.host, port=self.port, password=self.password, decode_responses=True)
                if self.password is not None
                else Redis(host=self.host, port=self.port, decode_responses=True)
            )

            logger.success("Redis connection created successfully.")

        except Exception as error:
            logger.error(f"Failed to create Redis connection: {error}")
            raise

    def _test(self) -> None:
        countdown = 0

        while True:
            try:
                logger.info("Testing Redis connection...")
                self.client.ping()
                logger.success("Redis connection is healthy.")
                break

            except Exception as error:
                if countdown != 3:
                    logger.warning("Redis connection test failed. Retrying in 5 seconds...")
                    countdown += 1
                    time.sleep(5)
                    continue

                logger.error(f"Failed to connect to Redis: {error}")
                raise

    def get_client(self) -> Redis:
        self._conn()
        self._test()
        return self.client
