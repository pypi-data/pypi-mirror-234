from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from faststream import Context, ContextRepo, FastStream, Logger
from faststream.kafka import KafkaBroker


class Point(BaseModel):
    x: float = Field(
        ..., examples=[0.5], description="The X Coordinate in the coordinate system"
    )
    y: float = Field(
        ..., examples=[0.5], description="The Y Coordinate in the coordinate system"
    )
    time: datetime = Field(
        ...,
        examples=["2020-04-23 10:20:30.400000"],
        description="The timestamp of the record",
    )


broker = KafkaBroker("localhost:9092")
app = FastStream(broker)


to_output_data = broker.publisher("output_data")


@app.on_startup
async def app_setup(context: ContextRepo):
    """
    Set all necessary global variables inside ContextRepo object:
        Set message_history for storing all input messages
    """
    raise NotImplementedError()


@broker.subscriber("input_data")
async def on_input_data(
    msg: Point,
    logger: Logger,
    message_history: List[Point] = Context(),
    key: bytes = Context("message.raw_message.key"),
) -> None:
    """
    Processes a message from the 'input_data' topic.
    Add all x elements from the memory (x_sum) and all y from the memory (y_sum) and publish the message with x_sum and y_sum to the output_data topic.
    The same partition key should be used in the input_data and output_data topic.

    Instructions:
    1. Consume a message from 'input_data' topic.
    2. Create a new message object (do not directly modify the original).
    3. Add all x elements from the memory (x_sum) and all y from the memory (y_sum)
    4. Publish the message with x_sum and y_sum to the output_data topic. (The same partition key should be used in the input_data and output_data topic).
    """
    raise NotImplementedError()
