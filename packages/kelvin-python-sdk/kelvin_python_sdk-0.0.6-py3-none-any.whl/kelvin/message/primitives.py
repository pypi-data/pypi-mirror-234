from kelvin.message.message import Message
from kelvin.message.msg_type import KMessageTypeData, KMessageTypeParameter


class Number(Message):
    _TYPE = KMessageTypeData("number")

    payload: float = 0.0


class String(Message):
    _TYPE = KMessageTypeData("string")

    payload: str = ""


class Boolean(Message):
    _TYPE = KMessageTypeData("boolean")

    payload: bool = False


class NumberParameter(Message):
    _TYPE = KMessageTypeParameter("number")

    payload: float = 0.0


class StringParameter(Message):
    _TYPE = KMessageTypeParameter("string")

    payload: str = ""


class BooleanParameter(Message):
    _TYPE = KMessageTypeParameter("boolean")

    payload: bool = False
