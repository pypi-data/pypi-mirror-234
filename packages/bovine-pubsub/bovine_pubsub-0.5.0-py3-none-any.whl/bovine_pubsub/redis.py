import asyncio
import logging
from quart_redis import get_redis

logger = logging.getLogger(__name__)


class RedisBovinePubSub:
    def __init__(self):
        self.health_pings = {}

    async def send(self, endpoint_path, data):
        redis = get_redis()
        await redis.publish(endpoint_path, data)

    async def event_stream(self, endpoint_path):
        task = asyncio.create_task(self.health_ping(endpoint_path))

        try:
            redis = get_redis()
            async with redis.pubsub() as pubsub:
                await pubsub.subscribe(endpoint_path)
                async for message in pubsub.listen():
                    if message["type"] == "message":
                        msg = message["data"]
                        yield msg
                        yield "\n".encode("utf-8")
        finally:
            logger.info("Cancelling task")
            task.cancel()

    async def health_ping(self, endpoint_path):
        while True:
            await asyncio.sleep(30)
            await self.send(endpoint_path, (":" + " " * 2048 + "\n").encode("utf-8"))
