import os
from quart_redis import RedisHandler

from .amqp import AmqpBovinePubSub
from .redis import RedisBovinePubSub
from .queue import QueueBovinePubSub


def BovinePubSub(app):
    redis_url = os.environ.get("BOVINE_REDIS")
    amqp_url = os.environ.get("BOVINE_AMQP")

    if amqp_url:
        app.config["AMQP_URI"] = amqp_url

        @app.before_serving
        async def configure_bovine_pub_sub_amqp():
            app.config["bovine_pub_sub"] = AmqpBovinePubSub(amqp_url)

        @app.after_serving
        async def shutdown_bovine_pub_sub_amqp():
            await app.config["bovine_pub_sub"].disconnect()

    elif redis_url:
        app.config["REDIS_URI"] = redis_url
        RedisHandler(app)

        @app.before_serving
        async def configure_bovine_pub_sub_redis():
            app.config["bovine_pub_sub"] = RedisBovinePubSub()

    else:

        @app.before_serving
        async def configure_bovine_pub_sub_queues():
            app.config["bovine_pub_sub"] = QueueBovinePubSub()
