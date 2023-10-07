import asyncio
import random
from asyncio import StreamReader, StreamWriter
from typing import List, Union

import yaml

from kelvin.message import KMessageTypeData, KRNAssetDataStream, Message
from kelvin.publisher.config import AppConfig


class Publisher:
    app_yaml: str
    app_config: AppConfig
    rand_min: float
    rand_max: float
    random: bool
    current_value: float

    def __init__(self, app_yaml: str, rand_min: float = 0, rand_max: float = 100, random: bool = True):
        self.app_yaml = app_yaml
        self.rand_min = rand_min
        self.rand_max = rand_max
        self.random = random
        self.current_value = 0.0
        with open(app_yaml) as f:
            config_yaml = yaml.safe_load(f)
            self.app_config = AppConfig(**config_yaml)

    def generate_random_value(self, data_type: str) -> Union[bool, float, str]:
        if data_type == "boolean":
            return random.choice([True, False])

        if self.random:
            number = round(random.random() * (self.rand_max - self.rand_min) + self.rand_min, 2)
        else:
            self.current_value = (self.current_value + 1) % (self.rand_max - self.rand_min) + self.rand_min
            number = self.current_value

        if data_type == "number":
            return number

        # if data_type == "string":
        return f"str_{number}"

    def get_all_messages(self) -> List[Message]:
        msgs: List[Message] = []

        default_assets = [asset.name for asset in self.app_config.app.kelvin.assets]
        for input in self.app_config.app.kelvin.inputs:
            for asset in default_assets:
                msgs.append(
                    Message(
                        type=KMessageTypeData(primitive=input.data_type),  # type: ignore
                        resource=KRNAssetDataStream(asset, input.name),
                        payload=self.generate_random_value(input.data_type),
                    )
                )

        return msgs


class PublisherServer:
    period_s: float
    publisher: Publisher
    running: bool

    def __init__(self, period_s: float, publisher: Publisher):
        self.period_s = period_s
        self.publisher = publisher
        self.running = False

    async def new_client(self, reader: StreamReader, writer: StreamWriter) -> None:
        if self.running is True:
            writer.close()
            return

        print("Client connected")
        self.running = True

        tasks = {
            asyncio.create_task(self.handle_read(reader)),
            asyncio.create_task(self.periodic_publisher(writer, self.period_s)),
        }

        await asyncio.gather(*tasks)

        self.running = False
        print("Client disconnected")

    async def periodic_publisher(self, writer: StreamWriter, period_s: float) -> None:
        while self.running and not writer.is_closing():
            msgs = self.publisher.get_all_messages()
            for msg in msgs:
                writer.write(msg.encode() + b"\n")

            try:
                await writer.drain()
            except ConnectionResetError:
                pass

            await asyncio.sleep(period_s)

    async def handle_read(self, reader: StreamReader) -> None:
        while self.running:
            data = await reader.readline()
            if not len(data):
                break
            try:
                msg = Message.parse_raw(data)
                print("Got new message", msg)
            except Exception as e:
                print("Error parsing message", e)
