from kelvin.app.filters import is_data_message
from kelvin.message import Number, NumberParameter


def test_is_data_message():
    assert is_data_message(Number(payload=1.0))
    assert is_data_message(NumberParameter(payload=1.0)) is False
