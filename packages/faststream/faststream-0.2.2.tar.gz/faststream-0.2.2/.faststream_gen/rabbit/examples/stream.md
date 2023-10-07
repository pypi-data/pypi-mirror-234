# RabbitMQ Streams

*RabbitMQ* has a [Streams](https://www.rabbitmq.com/streams.html){.exteranl-link target="_blank"} feature, which is closely related to *Kafka* topics.

The main difference from regular *RabbitMQ* queues is that the messages are not deleted after consuming.

And **FastStream** supports this feature as well!

```python linenums="1" hl_lines="4 10-12 17"
from faststream import FastStream, Logger
from faststream.rabbit import RabbitBroker, RabbitQueue

broker = RabbitBroker(max_consumers=10)
app = FastStream(broker)

queue = RabbitQueue(
    name="test-stream",
    durable=True,
    arguments={
        "x-queue-type": "stream",
    },
)


@broker.subscriber(
    queue,
    consume_args={"x-stream-offset": "first"},
)
async def handle(msg, logger: Logger):
    logger.info(msg)


@app.after_startup
async def test():
    await broker.publish("Hi!", queue)
```
