"""
Cria as operações do Redis
"""

import asyncio

from typing import Any, AsyncIterator

from redis import Redis
from redis.exceptions import WatchError

from src.logs.module import Logs


logger = Logs(loglevel="SUCCESS")


class RedisControl:

    def __init__(self, client: Redis) -> None:
        self.client = client

    async def incr(self, key: str, time: int | None = None) -> int:
        logger.info(f"Incrementando chave '{key}'...")

        expire = time if time is not None else 60

        while True:
            try:
                with self.client.pipeline(transaction=True) as session:
                    session.watch(key)

                    session.multi()
                    session.incr(key)
                    session.expire(key, expire)

                    result = session.execute()
                    value = result[0]

                    logger.success(f"Chave '{key}' incrementada com sucesso!")
                    return value

            except WatchError:
                logger.warning(f"A chave '{key}' foi alterada por outra operação. Tentando novamente...")

            except Exception as error:
                logger.error(f"Erro ao incrementar chave '{key}': {error}")
                raise

    async def hash(self, key: str, data: dict, time: int | None = None) -> None:
        logger.info(f"Salvando hash '{key}'...")

        expire = time if time is not None else 60

        while True:
            try:
                with self.client.pipeline(transaction=True) as session:
                    session.watch(key)

                    session.multi()
                    session.hset(key, mapping=data)
                    session.expire(key, expire)

                    session.execute()

                    logger.success(f"Hash '{key}' salvo com sucesso!")
                    return

            except WatchError:
                logger.warning(f"O hash '{key}' foi alterado por outra operação. Tentando novamente...")

            except Exception as error:
                logger.error(f"Erro ao salvar hash '{key}': {error}")
                raise

    async def read(self, key: str, hash: bool = False) -> Any:
        logger.info(f"Lendo chave '{key}'...")

        try:
            with self.client.pipeline(transaction=True) as session:
                session.multi()

                if hash:
                    session.hgetall(key)
                else:
                    session.get(key)

                result = session.execute()
                value = result[0]

                logger.success(f"Chave '{key}' lida com sucesso!")
                return value

        except Exception as error:
            logger.error(f"Erro ao ler chave '{key}': {error}")
            raise

    async def delete(self, key: str) -> bool:
        logger.info(f"Apagando cache '{key}'...")

        while True:
            try:
                with self.client.pipeline(transaction=True) as session:
                    session.watch(key)

                    session.multi()
                    session.delete(key)

                    result = session.execute()
                    deleted = bool(result[0])

                    logger.success(f"Cache '{key}' apagado com sucesso!")
                    return deleted

            except WatchError:
                logger.warning(f"A chave '{key}' foi alterada antes de ser apagada. Tentando novamente...")

            except Exception as error:
                logger.error(f"Erro ao apagar cache '{key}': {error}")
                raise

    async def publish(self, channel: str, event: str) -> int:
        logger.info(f"Publicando evento no canal '{channel}'...")

        try:
            with self.client.pipeline(transaction=True) as session:
                session.multi()
                session.publish(channel, event)

                result = session.execute()
                listeners = result[0]

                logger.success(f"Evento publicado no canal '{channel}' com sucesso!")
                return listeners

        except Exception as error:
            logger.error(f"Erro ao publicar evento no canal '{channel}': {error}")
            raise

    async def listen(self, channel: str) -> AsyncIterator[Any]:
        logger.info(f"Iniciando escuta do canal '{channel}'...")

        pubsub = self.client.pubsub()

        try:
            pubsub.subscribe(channel)

            logger.success(f"Escutando canal '{channel}'!")

            while True:
                message = await asyncio.to_thread(
                    pubsub.get_message,
                    ignore_subscribe_messages=True,
                    timeout=1
                )

                if message is None:
                    continue

                logger.info(f"Evento recebido no canal '{channel}'")
                yield message["data"]

        except Exception as error:
            logger.error(f"Erro ao escutar canal '{channel}': {error}")
            raise

        finally:
            try:
                pubsub.unsubscribe(channel)
                pubsub.close()

                logger.info(f"Escuta do canal '{channel}' encerrada")

            except Exception as error:
                logger.error(f"Erro ao encerrar Pub/Sub '{channel}': {error}")