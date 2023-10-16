from collections import defaultdict
import asyncio
import logging

logger = logging.getLogger(__name__)


class QueueBovinePubSub:
    def __init__(self):
        self.queues = defaultdict(asyncio.Queue)

    async def send(self, endpoint_path, data):
        await self.queues[endpoint_path].put(data)

    async def event_stream(self, endpoint_path):
        task = asyncio.create_task(self.health_ping(endpoint_path))

        try:
            while True:
                data = await self.queues[endpoint_path].get()
                yield data
                yield "\n".encode("utf-8")
        finally:
            logger.info("Cancelling task")
            task.cancel()

    async def health_ping(self, endpoint_path):
        while True:
            await asyncio.sleep(30)
            await self.send(endpoint_path, (":" + " " * 2048 + "\n").encode("utf-8"))
