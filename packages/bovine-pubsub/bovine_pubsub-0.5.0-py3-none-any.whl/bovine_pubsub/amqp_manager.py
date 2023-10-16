import aio_pika
from uuid import uuid4
from bovine import BovineClient

from .amqp_iterator import AmqpIterator


class AmqpManager:
    def __init__(self, amqp_uri, queue_name=None):
        self.amqp_uri = amqp_uri
        if queue_name:
            self.queue_name = queue_name
            self.auto_delete = False
            self.durable = True
        else:
            self.queue_name = str(uuid4())
            self.auto_delete = True
            self.durable = False

        self.clients = {}

    async def add_bovine_client(self, client: BovineClient):
        event_source = client.information["endpoints"]["eventSource"]

        self.clients[event_source] = client

        await self.queue.bind(
            self.exchange,
            routing_key=event_source,
        )

    async def init(self):
        self.connection = await aio_pika.connect(self.amqp_uri)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=10)
        self.exchange = await self.channel.declare_exchange(
            "processed",
            aio_pika.ExchangeType.TOPIC,
        )
        self.queue = await self.channel.declare_queue(
            self.queue_name, durable=self.durable, auto_delete=self.auto_delete
        )

    def iter(self):
        return AmqpIterator(self.queue, self.clients)

    @property
    def iterator(self):
        return self.queue.iterator()
