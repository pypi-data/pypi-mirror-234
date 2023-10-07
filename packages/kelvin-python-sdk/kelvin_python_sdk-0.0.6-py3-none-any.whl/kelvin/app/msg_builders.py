from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional, Union
from uuid import UUID, uuid4

from pydantic.dataclasses import dataclass
from pydantic.fields import Field

from kelvin.message import KRN, Message
from kelvin.message.base_messages import (
    ControlChangeMsg,
    ControlChangePayload,
    RecommendationActions,
    RecommendationControlChange,
    RecommendationMsg,
    RecommendationPayload,
)


class MessageBuilder(ABC):
    @abstractmethod
    def to_message(self) -> Message:
        pass


@dataclass
class ControlChange(MessageBuilder):
    """Control change builder
    Use this helper class to build a Kelvin Control change.

    Args:
        resource (KRN): The kelvin resource targed by the control change, represented by a KRN (usually
            KRNAssetDataStream)
        expiraton_date (datetime | timedelta): The absolute time in the future when the Control Change expires. Provide
            either a absolute datetime or a timedelta from now
        payload (bool, int, float, str): The desired target value for the control change
        retries (int): Optional number of retries
        timeout (int): Optional timeout time (for retries)
        control_change_id (UUID): Optional UUID to set an specific ID for the control change
    """

    resource: KRN
    expiration_date: Union[datetime, timedelta]
    payload: Union[bool, int, float, str]
    retries: Optional[int] = None
    timeout: Optional[int] = None
    control_change_id: Optional[UUID] = None

    def to_message(self) -> ControlChangeMsg:
        if isinstance(self.expiration_date, datetime):
            expiration = self.expiration_date
        else:
            expiration = datetime.now() + self.expiration_date

        return ControlChangeMsg(
            id=self.control_change_id if self.control_change_id is not None else uuid4(),
            resource=self.resource,
            payload=ControlChangePayload(
                timeout=self.timeout,
                retries=self.retries,
                expiration_date=expiration,
                payload=self.payload,
            ),
        )


@dataclass
class Recommendation(MessageBuilder):
    """Recommendation Builder. Use this helper class to build a Kelvin Recommendation.

    Args:
        resource (KRN): The kelvin resource targed by the recommendation, represented by a KRN (usually a KRNAsset)
        type (str): the type of the recommendation, chose one from the available on the kelvin platform (eg generic,
            speed_inc, speed_dec, ...)
        expiraton_date (datetime | timedelta): The absolute time in the future when the recommendation expires. Provide
            either a absolute datetime or a timedelta from now
        description (str): An optional description for the recommendation
        confidence (int): Optional confidence of the recommendation (from 1 to 4)
        control_changes (list[ControlChanges]): the list of ControlChanges associated with the recommendation
    """

    resource: KRN
    type: str
    expiration_date: Union[datetime, timedelta]
    description: Optional[str] = None
    confidence: Optional[int] = Field(default=None, ge=1, le=4)
    control_changes: List[ControlChange] = Field(default_factory=list)

    def to_message(self) -> RecommendationMsg:
        ccs = []
        for cc in self.control_changes:
            if isinstance(cc.expiration_date, datetime):
                cc_expiration = cc.expiration_date
            else:
                cc_expiration = datetime.now() + cc.expiration_date
            ccs.append(
                RecommendationControlChange(
                    retry=cc.retries,
                    timeout=cc.timeout,
                    expiration_date=cc_expiration,
                    payload=cc.payload,
                    resource=cc.resource,
                    control_change_id=cc.control_change_id,
                )
            )
        if isinstance(self.expiration_date, datetime):
            rec_expiration_date = self.expiration_date
        else:
            rec_expiration_date = datetime.now() + self.expiration_date

        return RecommendationMsg(
            resource=self.resource,
            payload=RecommendationPayload(
                resource=self.resource,
                type=self.type,
                description=self.description,
                expiration_date=rec_expiration_date,
                confidence=self.confidence,
                actions=RecommendationActions(control_changes=ccs),
            ),
        )
