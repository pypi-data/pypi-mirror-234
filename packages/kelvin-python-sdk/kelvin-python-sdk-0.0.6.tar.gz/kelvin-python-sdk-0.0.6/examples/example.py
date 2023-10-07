from __future__ import annotations

import asyncio
import random
from asyncio import Queue
from datetime import datetime, timedelta

from kelvin.app import ControlChange, KelvinApp, Recommendation, filters
from kelvin.message import Boolean, KRNAsset, KRNAssetDataStream, KRNWorkload, Message, Number, String


async def on_connect() -> None:
    print("Hello, it's connected")


async def on_disconnect() -> None:
    print("Hello, it's disconnected")


# Takes Data Messages from KRNAssetDataStream("asset1", "input-number"), doubles its value and publishes it as "output-number"
async def double_msg_value(cli: KelvinApp, queue: Queue[Number]) -> None:
    while True:
        msg = await queue.get()
        print("Received Input: ", msg)

        # Publish Data (Number)
        await cli.publish(
            Number(resource=KRNAssetDataStream(msg.resource.asset, "output-number"), payload=msg.payload * 2)
        )


async def log_parameters(queue: Queue[Message]) -> None:
    while True:
        msg = await queue.get()

        print("Receive parameter: ", msg)


async def main() -> None:
    # Creatiing instance of Kelvin App Client
    cli = KelvinApp()

    # Setting Basic App Client Callbacks
    cli.on_connect = on_connect
    cli.on_disconnect = on_disconnect

    # Creating a filter for a specific resource (krn)
    my_message_filter = cli.filter(filters.resource_equal(KRNAssetDataStream("asset1", "input-number")))
    # Creating async task handling the data filtered above ^
    asyncio.create_task(double_msg_value(cli, my_message_filter))

    # Creating a filter for parameter messages
    my_parameter_filter = cli.filter(filters.is_parameter)
    # Creating async task handling the parameter messages filteres above ^
    asyncio.create_task(log_parameters(my_parameter_filter))

    # Connect the App Client
    await cli.connect()

    # Custom Loop
    while True:
        random_value = round(random.random() * 10, 2)

        # Publish Data (Number)
        await cli.publish(Number(resource=KRNAssetDataStream("asset1", "output-random-number"), payload=random_value))

        # Publish Data (String)
        await cli.publish(
            String(resource=KRNAssetDataStream("asset1", "output-random-string"), payload=str(random_value))
        )

        # Publish Data (Boolean)
        await cli.publish(
            Boolean(
                resource=KRNAssetDataStream("asset1", "output-random-boolean"), payload=random.choice([True, False])
            )
        )

        expiration_date = datetime.now() + timedelta(minutes=10)

        # Publish Control Change
        await cli.publish(
            ControlChange(
                expiration_date=expiration_date,
                resource=KRNAssetDataStream("asset1", "output-cc-number"),
                payload=random_value,
            )
        )

        # Publish Recommendation
        await cli.publish(
            Recommendation(
                type="generic",
                resource=KRNAsset("asset1"),
                expiration_date=timedelta(minutes=10),
                control_changes=[
                    ControlChange(
                        resource=KRNAssetDataStream("asset1", "output-cc-number"),
                        expiration_date=expiration_date,
                        retries=0,
                        timeout=300,
                        payload=random_value + 1,
                    )
                ],
            )
        )

        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
