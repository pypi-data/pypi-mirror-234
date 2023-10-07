# Custom Parser

At this stage, **FastStream** serializes an incoming message from the broker's framework into a general format called **StreamMessage**. During this stage, the message body remains in the form of raw bytes.

**StreamMessage** is a general representation of a message within **FastStream**. It contains all the information required for message processing within **FastStreams**.  It is even used to represent message batches, so the primary reason to customize it is to redefine the metadata associated with **FastStream** messages.

For example, you can specify your own header with the `message_id` semantic. This allows you to inform **FastStream** about this custom header through parser customization.

## Signature

To create a custom message parser, you should write a regular Python function (synchronous or asynchronous) with the following signature:

=== "Kafka"
    ``` python
    from aiokafka import ConsumerRecord
    from faststream.kafka import KafkaMessage

    def parser(msg: ConsumerRecord) -> KafkaMessage:
        ...
    ```

=== "RabbitMQ"
    ``` python
    from aio_pika import IncomingMessage
    from faststream.rabbit import RabbitMessage

    def parser(msg: IncomingMessage) -> RabbitMessage:
        ...
    ```

=== "NATS"
    ``` python
    from nats.aio.msg import Msg
    from faststream.nats import NatsMessage

    def parser(msg: Msg) -> NatsMessage:
        ...
    ```

Alternatively, you can reuse the original parser function with the following signature:

=== "Kafka"
    ``` python
    from types import Callable, Awaitable
    from aiokafka import ConsumerRecord
    from faststream.kafka import KafkaMessage

    async def parser(
        msg: ConsumerRecord,
        original_parser: Callable[[ConsumerRecord], Awaitable[KafkaMessage]],
    ) -> KafkaMessage:
        return await original_parser(msg)
    ```

=== "RabbitMQ"
    ``` python
    from types import Callable, Awaitable
    from aio_pika import IncomingMessage
    from faststream.rabbit import RabbitMessage

    async def parser(
        msg: IncomingMessage,
        original_parser: Callable[[IncomingMessage], Awaitable[RabbitMessage]],
    ) -> RabbitMessage:
        return await original_parser(msg)
    ```

=== "NATS"
    ``` python
    from types import Callable, Awaitable
    from nats.aio.msg import Msg
    from faststream.nats import NatsMessage

    async def parser(
        msg: Msg,
        original_parser: Callable[[Msg], Awaitable[NatsMessage]],
    ) -> RabbitMessage:
        return await original_parser(msg)
    ```

The argument naming doesn't matter; the parser will always be placed as the second argument.

!!! note
    The original parser is always an asynchronous function, so your custom parser should also be asynchronous.

Afterward, you can set this custom parser at the broker or subscriber level.

## Example

As an example, let's redefine `message_id` to a custom header:


=== "Kafka"
    ``` python linenums="1" hl_lines="9-15 18 28"
    {!> docs_src/getting_started/serialization/parser_kafka.py !}
    ```

=== "RabbitMQ"
    ``` python linenums="1" hl_lines="9-15 18 28"
    {!> docs_src/getting_started/serialization/parser_rabbit.py !}
    ```

=== "NATS"
    ``` python linenums="1" hl_lines="9-15 18 28"
    {!> docs_src/getting_started/serialization/parser_nats.py !}
    ```
