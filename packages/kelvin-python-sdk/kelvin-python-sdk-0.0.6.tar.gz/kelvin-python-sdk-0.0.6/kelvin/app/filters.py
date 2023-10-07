from __future__ import annotations

from typing import Callable

from typing_extensions import TypeAlias

from kelvin.message import KRN, KMessageTypeData, KMessageTypeParameter, Message

KelvinFilterType: TypeAlias = Callable[[Message], bool]


def is_data_message(msg: Message) -> bool:
    return isinstance(msg.type, KMessageTypeData)


def is_parameter(msg: Message) -> bool:
    return isinstance(msg.type, KMessageTypeParameter)


def resource_equal(resource: KRN) -> KelvinFilterType:
    return lambda msg: msg.resource == resource
