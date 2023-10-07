from pydantic import BaseModel, Field

from faststream import FastStream, Logger
from faststream.kafka import KafkaBroker


class Point(BaseModel):
    x: float = Field(
        ..., examples=[0.5], description="The X Coordinate in the coordinate system"
    )
    y: float = Field(
        ..., examples=[0.5], description="The Y Coordinate in the coordinate system"
    )


broker = KafkaBroker("localhost:9092")
app = FastStream(broker)


to_output_data = broker.publisher("output_data")


@broker.subscriber("input_data")
async def on_input_data(msg: Point, logger: Logger) -> None:
    """
    Processes a message from the 'input_data' topic.
    Increment msg x and y attributes with 1 and publish that message to the output_data topic.
    Publish that message to the output_data topic
    Use messages attribute x as a partition key when publishing to output_data topic.

    Instructions:
    1. Consume a message from 'input_data' topic.
    2. Create a new message object (do not directly modify the original).
    3. Increment msg x and y attributes with 1.
    4. Publish that message to the output_data topic (Use messages attribute x as a partition key).
    """
    raise NotImplementedError()
