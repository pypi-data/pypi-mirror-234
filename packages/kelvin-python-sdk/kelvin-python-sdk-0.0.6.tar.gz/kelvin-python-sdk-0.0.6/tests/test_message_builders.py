""" Test Message Builders """


from datetime import datetime, timedelta

from kelvin.app import ControlChange, Recommendation
from kelvin.message import ControlChangeMsg as ControlChangeMsg
from kelvin.message import KRNAsset, KRNAssetDataStream


def test_builder_control_change() -> None:
    now = datetime.now()

    cc = ControlChange(resource=KRNAssetDataStream("asset1", "metric1"), expiration_date=now, payload=25)

    cc_msg = cc.to_message()

    assert isinstance(cc_msg, ControlChangeMsg)
    assert cc_msg.payload.expiration_date == cc.expiration_date
    assert cc_msg.payload.payload == cc.payload
    assert cc_msg.resource == cc.resource


def test_builder_recommendation() -> None:
    now = datetime.now()

    cc = ControlChange(resource=KRNAssetDataStream("asset1", "metric1"), expiration_date=now, payload=25)

    cc_msg = cc.to_message()

    assert isinstance(cc_msg, ControlChangeMsg)
    assert cc_msg.payload.expiration_date == cc.expiration_date
    assert cc_msg.payload.payload == cc.payload
    assert cc_msg.resource == cc.resource
