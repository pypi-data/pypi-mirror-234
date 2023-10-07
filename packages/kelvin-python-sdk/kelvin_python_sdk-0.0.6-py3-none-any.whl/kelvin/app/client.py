from __future__ import annotations

import asyncio
from asyncio import Event, Queue
from typing import Any, AsyncGenerator, Awaitable, Callable, Optional, Tuple, Union, cast

from typing_extensions import TypeAlias

from kelvin.app import filters
from kelvin.app.msg_builders import MessageBuilder
from kelvin.app.stream import KelvinStream, KelvinStreamConfig
from kelvin.logs import get_logger
from kelvin.message import KRN, KRNAssetParameter, Message

logger = get_logger(__name__)

NoneCallbackType: TypeAlias = Optional[Callable[..., Awaitable[None]]]
MessageCallbackType: TypeAlias = Optional[Callable[[Message], Awaitable[None]]]


class KelvinApp:
    """Kelvin Client to connect to the Apllication Stream.
    Use this class to connect and interface with the Kelvin Stream.

    After connecting, the connection is handled automatically in the background.

    Use filters or filter_stream to easily listen for specific messages.
    Use register_callback methods to register callbacks for events like connect and disconnect.
    """

    READ_CYCLE_TIMEOUT_S = 0.25
    RECONNECT_TIMEOUT_S = 3

    def __init__(self, config: KelvinStreamConfig = KelvinStreamConfig()) -> None:
        self._stream = KelvinStream(config)
        self._filters: list[Tuple[Queue, filters.KelvinFilterType]] = []

        # map of asset name to map of parameter name to parameter message
        self._asset_parameters: dict[str, dict[str, Message]] = {}
        # map of app name to map of parameter name to parameter message
        self._app_parameters: dict[str, dict[str, Message]] = {}

        self.on_connect: NoneCallbackType = None
        self.on_disconnect: NoneCallbackType = None

        # todo: too many message callbacks? maybe we need dynamic callbacks like filters?
        self.on_message: MessageCallbackType = None
        self.on_data: MessageCallbackType = None
        self.on_control_change: MessageCallbackType = None

        self.on_asset_parameter: MessageCallbackType = None
        self.on_app_parameter: MessageCallbackType = None

        self.connected = Event()

    async def connect(self) -> None:
        """Connects to Kelvin Stream."""
        self._is_to_connect = True
        self._conn_task = asyncio.create_task(self._handle_connection())

    async def disconnect(self) -> None:
        """Disconnects from Kelvin Stream"""
        self._is_to_connect = False
        await self._conn_task

    @property
    def asset_parameters(self) -> dict[str, dict[str, Message]]:
        return self._asset_parameters

    @property
    def app_parameters(self) -> dict[str, dict[str, Message]]:
        return self._app_parameters

    async def __aenter__(self) -> KelvinApp:
        await self.connect()
        return self

    async def __aexit__(self, *args: Any) -> bool:
        await self.disconnect()
        return True

    async def _handle_connection(self) -> None:
        while self._is_to_connect:
            try:
                try:
                    await self._stream.connect()
                except ConnectionError:
                    logger.error(f"Error connecting, reconnecting in {self.RECONNECT_TIMEOUT_S} sec.")
                    await asyncio.sleep(self.RECONNECT_TIMEOUT_S)
                    continue

                self.connected.set()
                if self.on_connect:
                    await self.on_connect()

                await self._handle_read()

                self.connected.clear()
                if self.on_disconnect:
                    await self.on_disconnect()
            except Exception:
                logger.exception("Unexpected error on connection handler")
                await asyncio.sleep(self.RECONNECT_TIMEOUT_S)

    async def _handle_read(self) -> None:
        while self._is_to_connect:
            try:
                msg = await asyncio.wait_for(self._stream.read(), timeout=self.READ_CYCLE_TIMEOUT_S)
            except asyncio.TimeoutError:
                continue
            except ConnectionError:
                break

            await self._process_message(msg)

            self._route_to_filters(msg)

    def _msg_is_control_change(self, msg: Message) -> bool:
        # todo: implement when we know how to check if the message is control changes
        # we need the app configuration to know this
        return False

    def _build_parameter_map(self, asset: bool, msg: Message) -> None:
        # Unflatten the parameter name from the nested a.b.c to a dict of {a: {b: {c: msg}}}
        if msg and msg.resource:
            if asset:
                self._asset_parameters = expand_map(self._asset_parameters, build_nested_map(msg))
            else:
                self._app_parameters = expand_map(self._app_parameters, build_nested_map(msg))

    async def _process_message(self, msg: Message) -> None:
        if self.on_message:
            await self.on_message(msg)

        if filters.is_parameter(msg):
            # determine if it's an asset or app parameter and store it
            asset = isinstance(msg.resource, KRNAssetParameter)
            self._build_parameter_map(asset, msg)
            if asset:
                if self.on_asset_parameter:
                    await self.on_asset_parameter(msg)
            else:
                if self.on_app_parameter:
                    await self.on_app_parameter(msg)
            return

        if self.on_control_change and self._msg_is_control_change(msg):
            await self.on_control_change(msg)
            return

        if self.on_data and filters.is_data_message(msg):
            await self.on_data(msg)
            return

    def _route_to_filters(self, msg: Message) -> None:
        for queue, func in self._filters:
            if func(msg) is True:
                # todo: check if the message is reference
                queue.put_nowait(msg)

    def filter(self, func: filters.KelvinFilterType) -> Queue[Message]:
        """Creates a filter for the received Kelvin Messages based on a filter function.

        Args:
            func (filters.KelvinFilterType): Filter function, it should receive a Message as argument and return bool.

        Returns:
            Queue[Message]: Returns a asyncio queue to receive the filtered messages.
        """
        queue: Queue = Queue()
        self._filters.append((queue, func))
        return queue

    def stream_filter(self, func: filters.KelvinFilterType) -> AsyncGenerator[Message, None]:
        """Creates a filter for the received Kelvin Messages based on a filter function.
        See filter.

        Args:
            func (filters.KelvinFilterType): Filter function, it should receive a Message as argument and return bool.

        Returns:
            AsyncGenerator[Message, None]: Async Generator that can be async iterated to receive filtered messages.

        Yields:
            Iterator[AsyncGenerator[Message, None]]: Yields the filtered messages.
        """
        queue = self.filter(func)

        async def _generator() -> AsyncGenerator[Message, None]:
            while True:
                msg = await queue.get()
                yield msg

        return _generator()

    async def publish(self, msg: Union[Message, MessageBuilder]) -> bool:
        """Publishes a Message to Kelvin Stream

        Args:
            msg (Message): Kelvin Message to publish

        Returns:
            bool: True if the message was sent with success.
        """
        try:
            if isinstance(msg, MessageBuilder):
                m = msg.to_message()
            else:
                m = msg

            return await self._stream.write(m)
        except ConnectionError:
            logger.error("Failed to publish message, connection is unavailable.")
            return False


def build_nested_map(msg: Message) -> dict[str, Any]:
    # build_nested_map takes in a message with a dot-delimited namespace and returns a nested dictionary
    # with the namespace as keys and the message as the value
    n = cast(KRN, msg.resource).ns_string.split(".")
    ret: dict[str, Any] = {}
    ref = ret
    for i in range(len(n)):
        if i == len(n) - 1:  # terminate - update the last key with the message
            ref[n[i]] = msg
        else:
            # if the key doesn't exist, create a new dictionary
            ref[n[i]] = ref.get(n[i], {})

        # update the reference to the next level
        ref = ref[n[i]]
    return ret


def expand_map(entry: dict[str, Any], expansion: dict[str, Any]) -> dict[str, Any]:
    # expand_map takes an existing dictionary (such as {a: {b: {c: msg}}}) and expands it with the new dictionary
    # (such as {a: {b: {d: msg}}}) to produce {a: {b: {c: msg, d: msg}}}
    ref = expansion.copy()
    if entry:
        for key, value in ref.items():
            if key in entry:
                if isinstance(entry[key], dict):
                    entry.update({key: expand_map(entry[key], value)})
                else:
                    entry[key] = expansion[key]
            else:
                entry[key] = value
        return entry
    else:
        return expansion
