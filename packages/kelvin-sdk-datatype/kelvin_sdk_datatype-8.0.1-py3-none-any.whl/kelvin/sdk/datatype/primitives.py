from kelvin.sdk.datatype.message import Message
from kelvin.sdk.datatype.msg_type import KMessageTypeData, KMessageTypeParameter


class Number(Message):
    _TYPE = KMessageTypeData("number")

    payload: float = 0.0


class String(Message):
    _TYPE = KMessageTypeData("string")

    payload: str = ""


class PrimitiveBoolean(Message):
    _TYPE = KMessageTypeData("boolean")

    payload: bool = False


class Integer(Message):
    _TYPE = KMessageTypeData("integer")

    payload: int = 0


class NumberParameter(Message):
    _TYPE = KMessageTypeParameter("number")

    payload: float = 0.0


class StringParameter(Message):
    _TYPE = KMessageTypeParameter("string")

    payload: str = ""


class BooleanParameter(Message):
    _TYPE = KMessageTypeParameter("boolean")

    payload: bool = False


class IntegerParameter(Message):
    _TYPE = KMessageTypeParameter("integer")

    payload: int = 0
