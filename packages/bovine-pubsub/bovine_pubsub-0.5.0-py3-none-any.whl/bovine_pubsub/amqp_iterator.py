import asyncio
import json
import logging
from bovine.types import ServerSentEvent

logger = logging.getLogger(__name__)


class AmqpIterator:
    def __init__(self, queue, clients):
        self.clients = clients
        self.queue = queue.iterator()

    async def __aenter__(self):
        await self.queue.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.queue.__aexit__(exc_type, exc_val, exc_tb)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            message = await self.queue.__anext__()

            async with message.process():
                client = self.clients.get(message.routing_key)
                if client:
                    body = message.body.decode("utf-8")
                    event = ServerSentEvent.parse_utf8(body)

            return client, json.loads(event.data)
        except asyncio.exceptions.CancelledError:
            logger.warning("Cancelled")
            return None, None
        except Exception as e:
            logger.exception(e)
            return None, None
