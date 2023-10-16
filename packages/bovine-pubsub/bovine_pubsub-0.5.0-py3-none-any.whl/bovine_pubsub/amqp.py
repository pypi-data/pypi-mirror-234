import logging
import aio_pika
import asyncio

from uuid import uuid4

logger = logging.getLogger(__name__)


class AmqpBovinePubSub:
    def __init__(self, amqp_uri):
        self.amqp_uri = amqp_uri
        self.connection = None
        self.heartbeat_task = asyncio.create_task(self.heartbeat())

    async def disconnect(self):
        self.heartbeat_task.cancel()

    async def heartbeat(self):
        connection = await aio_pika.connect_robust(self.amqp_uri)
        async with connection:
            channel = await connection.channel()

            processed_exchange = await channel.declare_exchange(
                "processed",
                aio_pika.ExchangeType.TOPIC,
            )

            while True:
                await processed_exchange.publish(
                    aio_pika.Message(
                        body=": mooo".encode("utf-8"),
                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    ),
                    routing_key="heartbeat",
                )
                await asyncio.sleep(15)

    async def send(self, endpoint_path, data):
        connection = await aio_pika.connect_robust(self.amqp_uri)
        async with connection:
            channel = await connection.channel()

            processed_exchange = await channel.declare_exchange(
                "processed",
                aio_pika.ExchangeType.TOPIC,
            )

            await processed_exchange.publish(
                aio_pika.Message(
                    body=data,
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                ),
                routing_key=endpoint_path,
            )

    async def event_stream(self, endpoint_path):
        try:
            connection = await aio_pika.connect_robust(self.amqp_uri)
            async with connection:
                channel = await connection.channel()
                await channel.set_qos(prefetch_count=10)
                processed_exchange = await channel.declare_exchange(
                    "processed",
                    aio_pika.ExchangeType.TOPIC,
                )
                queue_name = str(uuid4())
                logger.info("Creating queue %s", queue_name)
                queue = await channel.declare_queue(
                    queue_name, auto_delete=True, durable=False
                )
                # await asyncio.sleep(0.3)
                await queue.bind(processed_exchange, routing_key=endpoint_path)
                await queue.bind(processed_exchange, routing_key="heartbeat")
                logger.info("Bounnd ququq %s to topic %s", queue_name, endpoint_path)
                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        async with message.process():
                            body = message.body
                            yield body
                            yield "\n".encode("utf-8")
        except Exception as e:
            logger.exception(e)
