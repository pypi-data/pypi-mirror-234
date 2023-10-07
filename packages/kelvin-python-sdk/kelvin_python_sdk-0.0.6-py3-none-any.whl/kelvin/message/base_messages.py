from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator

from kelvin.message.krn import KRN
from kelvin.message.message import Message
from kelvin.message.msg_type import (
    KMessageTypeControl,
    KMessageTypeControlStatus,
    KMessageTypeData,
    KMessageTypeRecommendation,
)
from kelvin.message.utils import from_rfc3339_timestamp, to_rfc3339_timestamp


class ControlChangePayload(BaseModel):
    timeout: Optional[int] = Field(description="Timeout for retries")
    retries: Optional[int] = Field(description="Max retries")
    expiration_date: datetime = Field(decription="Absolutc expiration Date in UTC")
    payload: Any = Field(None, description="Control Change payload")

    class Config:
        json_encoders = {datetime: to_rfc3339_timestamp}

    @validator("expiration_date", pre=True, always=True)
    def parse_expiration_date(cls, v: Union[str, datetime]) -> datetime:
        if isinstance(v, str):
            return from_rfc3339_timestamp(v)
        return v


class ControlChangeMsg(Message):
    """Generic Control Change Message"""

    _TYPE = KMessageTypeControl()

    payload: ControlChangePayload


class StateEnum(str, Enum):
    ready = "ready"
    sent = "sent"
    failed = "failed"
    processed = "processed"
    applied = "applied"


class ControlChangeStatusPayload(BaseModel):
    state: StateEnum
    message: Optional[str] = Field(decription="")
    payload: Any = Field(None, description="Metric value at status time")


class ControlChangeStatus(Message):
    """Generic Control Change Message"""

    _TYPE = KMessageTypeControlStatus()

    payload: ControlChangeStatusPayload


class SensorDataPayload(BaseModel):
    data: List[float] = Field(..., description="Array of sensor measurements.", min_items=1)
    sample_rate: float = Field(..., description="Sensor sample-rate in Hertz.", gt=0.0)


class SensorDataMsg(Message):
    """Sensor data."""

    _TYPE = KMessageTypeData("object", "kelvin.sensor_data")

    payload: SensorDataPayload


class RecommendationControlChange(ControlChangePayload):
    retries: Optional[int] = Field(description="Max retries", alias="retry")
    state: Optional[str]
    resource: Optional[KRN]
    control_change_id: Optional[str] = Field(description="Control Change ID")


class RecommendationActions(BaseModel):
    control_changes: List[RecommendationControlChange] = []


class RecommendationPayload(BaseModel):
    source: Optional[KRN]
    resource: KRN
    type: str
    description: Optional[str]
    confidence: Optional[int] = Field(ge=1, le=4)
    expiration_date: Optional[datetime]
    actions: RecommendationActions = RecommendationActions()
    metadata: Dict[str, Any] = {}

    class Config:
        json_encoders = {datetime: to_rfc3339_timestamp}

    @validator("expiration_date", pre=True, always=True)
    def parse_expiration_date(cls, v: Union[str, datetime]) -> datetime:
        if isinstance(v, str):
            return from_rfc3339_timestamp(v)
        return v


class RecommendationMsg(Message):
    _TYPE = KMessageTypeRecommendation()

    payload: RecommendationPayload
