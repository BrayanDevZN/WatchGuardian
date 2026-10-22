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
        logger.info(f"Incrementing key '{key}'...")

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

                    logger.success(f"Key '{key}' incremented successfully.")
                    return value

            except WatchError:
                logger.warning(f"Key '{key}' was modified by another operation. Retrying...")

            except Exception as error:
                logger.error(f"Failed to increment key '{key}': {error}")
                raise

    async def hash(self, key: str, data: dict, time: int | None = None) -> None:
        logger.info(f"Saving hash '{key}'...")

        expire = time if time is not None else 60

        while True:
            try:
                with self.client.pipeline(transaction=True) as session:
                    session.watch(key)

                    session.multi()
                    session.hset(key, mapping=data)
                    session.expire(key, expire)

                    session.execute()

                    logger.success(f"Hash '{key}' saved successfully.")
                    return

            except WatchError:
                logger.warning(f"Hash '{key}' was modified by another operation. Retrying...")

            except Exception as error:
                logger.error(f"Failed to save hash '{key}': {error}")
                raise

    async def read(self, key: str, hash: bool = False) -> Any:
        logger.info(f"Reading key '{key}'...")

        try:
            with self.client.pipeline(transaction=True) as session:
                session.multi()

                if hash:
                    session.hgetall(key)
                else:
                    session.get(key)

                result = session.execute()
                value = result[0]

                logger.success(f"Key '{key}' read successfully.")
                return value

        except Exception as error:
            logger.error(f"Failed to read key '{key}': {error}")
            raise

    async def delete(self, key: str) -> bool:
        logger.info(f"Deleting cache key '{key}'...")

        while True:
            try:
                with self.client.pipeline(transaction=True) as session:
                    session.watch(key)

                    session.multi()
                    session.delete(key)

                    result = session.execute()
                    deleted = bool(result[0])

                    logger.success(f"Cache key '{key}' deleted successfully.")
                    return deleted

            except WatchError:
                logger.warning(f"Key '{key}' was modified before deletion. Retrying...")

            except Exception as error:
                logger.error(f"Failed to delete cache key '{key}': {error}")
                raise

    async def publish(self, channel: str, event: str) -> int:
        logger.info(f"Publishing event to channel '{channel}'...")

        try:
            with self.client.pipeline(transaction=True) as session:
                session.multi()
                session.publish(channel, event)

                result = session.execute()
                listeners = result[0]

                logger.success(f"Event published to channel '{channel}' successfully.")
                return listeners

        except Exception as error:
            logger.error(f"Failed to publish event to channel '{channel}': {error}")
            raise

    async def listen(self, channel: str) -> AsyncIterator[Any]:
        logger.info(f"Starting listener for channel '{channel}'...")

        pubsub = self.client.pubsub()

        try:
            pubsub.subscribe(channel)

            logger.success(f"Listening to channel '{channel}'.")

            while True:
                message = await asyncio.to_thread(
                    pubsub.get_message,
                    ignore_subscribe_messages=True,
                    timeout=1
                )

                if message is None:
                    continue

                logger.info(f"Event received on channel '{channel}'.")
                yield message["data"]

        except Exception as error:
            logger.error(f"Failed while listening to channel '{channel}': {error}")
            raise

        finally:
            try:
                pubsub.unsubscribe(channel)
                pubsub.close()

                logger.info(f"Listener for channel '{channel}' closed.")

            except Exception as error:
                logger.error(f"Failed to close Pub/Sub channel '{channel}': {error}")