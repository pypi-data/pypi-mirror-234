# bovine_pubsub

bovine_pubsub is a simple wrapper to enable [server sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events) in bovine. These are used to communicate real time with clients without forcing them to use polling. If multiple workers are used with `bovine`, one needs to use Redis as the implementation with queues only works for a single process.

Starting with `bovine-pubsub` support for server side clients is available using AMQP. See `examples/bovine_listen.py` for details.

## Usage

The simplest usage example is given by

```python
from quart import Quart
from bovine_pubsub import BovinePubSub

app = Quart(__name__)
BovinePubSub(app)
```

it adds the config variable `app.config["bovine_pub_sub"]` to the Quart application. By calling

```python
await app.config["bovine_pub_sub"].send("channel:test", b"test")
```

one sends the bytes `b"test"` to the channel `channel:test`. By calling

```python
pub_sub.event_stream("channel:test")
```

one receives an async iterator that can be used as server sent events.

## Example usage

A usage example is provided by `examples/basic_app.py`. By running

```bash
python examples/basic.app
```

one can start a server that sends "test" 10 times a new socket is opened on `localhost:5000`. The above implementation will use the local queues. To use with Redis start

```bash
BOVINE_REDIS=redis://localhost:6379 python examples/basic_app.py 
```

with an appropriate value for the environment variable `BOVINE_REDIS`.

## Running tests

Testing redis can be done inside of the docker compose setup, e.g.

```bash
docker compose up -d
docker compose run main /bin/sh
cd bovine_pubsub
poetry install
poetry run pytest
BOVINE_REDIS=redis://redis:6379 poetry run pytest
BOVINE_AMQP=amqp://rabbitmq poetry run pytest
```
