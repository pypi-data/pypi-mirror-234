# Publishing in Batches

## General overview

If you need to send your data in batches, the @broker.publisher(...) decorator offers a convenient way to achieve this. To enable batch production, you need to perform two crucial steps:

Step 1: When creating your publisher, set the batch argument to True. This configuration tells the publisher that you intend to send messages in batches.

Step 2: In your producer function, return a tuple containing the messages you want to send as a batch. This action triggers the producer to gather the messages and transmit them as a batch to a Kafka broker.

Let's delve into a detailed example illustrating how to produce messages in batches to the output_data topic while consuming from the input_data_1 topic.

## Code example

First, lets take a look at the whole app creation and then dive deep into the steps for producing in batches, here is the application code:

```python linenums="1"
from typing import Tuple

from pydantic import BaseModel, Field, NonNegativeFloat

from faststream import FastStream, Logger
from faststream.kafka import KafkaBroker


class Data(BaseModel):
    data: NonNegativeFloat = Field(
        ..., examples=[0.5], description="Float data example"
    )


broker = KafkaBroker("localhost:9092")
app = FastStream(broker)


decrease_and_increase = broker.publisher("output_data", batch=True)


@decrease_and_increase
@broker.subscriber("input_data_1")
async def on_input_data_1(msg: Data, logger: Logger) -> Tuple[Data, Data]:
    logger.info(msg)
    return Data(data=(msg.data * 0.5)), Data(data=(msg.data * 2.0))


@broker.subscriber("input_data_2")
async def on_input_data_2(msg: Data, logger: Logger) -> None:
    logger.info(msg)
    await decrease_and_increase.publish(
        Data(data=(msg.data * 0.5)), Data(data=(msg.data * 2.0))
    )
```

Below, we have highlighted key lines of code that demonstrate the steps involved in creating and using a batch publisher:

Step 1: Creation of the Publisher

```python linenums="1"
decrease_and_increase = broker.publisher("output_data", batch=True)
```

Step 2: Publishing an Actual Batch of Messages

You can publish a batch by directly calling the publisher with a batch of messages you want to publish, like shown here:

```python linenums="1"
    await decrease_and_increase.publish(
        Data(data=(msg.data * 0.5)), Data(data=(msg.data * 2.0))
    )
```

Or you can decorate your processing function and return a batch of messages like shown here:

```python linenums="1"
@decrease_and_increase
@broker.subscriber("input_data_1")
async def on_input_data_1(msg: Data, logger: Logger) -> Tuple[Data, Data]:
    logger.info(msg)
    return Data(data=(msg.data * 0.5)), Data(data=(msg.data * 2.0))
```

The application in the example imelements both of these ways, feel free to use whatever option fits your needs better.

## Why publish in batches?

In this example, we've explored how to leverage the @broker.publisher decorator to efficiently publish messages in batches using FastStream and Kafka. By following the two key steps outlined in the previous sections, you can significantly enhance the performance and reliability of your Kafka-based applications.

Publishing messages in batches offers several advantages when working with Kafka:

1. Improved Throughput: Batch publishing allows you to send multiple messages in a single transmission, reducing the overhead associated with individual message delivery. This leads to improved throughput and lower latency in your Kafka applications.

2. Reduced Network and Broker Load: Sending messages in batches reduces the number of network calls and broker interactions. This optimization minimizes the load on the Kafka brokers and network resources, making your Kafka cluster more efficient.

3. Atomicity: Batches ensure that a group of related messages is processed together or not at all. This atomicity can be crucial in scenarios where message processing needs to maintain data consistency and integrity.

4. Enhanced Scalability: With batch publishing, you can efficiently scale your Kafka applications to handle high message volumes. By sending messages in larger chunks, you can make the most of Kafka's parallelism and partitioning capabilities.
