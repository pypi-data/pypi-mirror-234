from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator

from kelvin.sdk.datatype.krn import KRN
from kelvin.sdk.datatype.message import Message
from kelvin.sdk.datatype.msg_type import (
    KMessageTypeControl,
    KMessageTypeControlStatus,
    KMessageTypeData,
    KMessageTypeRecommendation,
)
from kelvin.sdk.datatype.utils import from_rfc3339_timestamp, to_rfc3339_timestamp

from kelvin.sdk.datatype.types import (  # isort:skip
    Float32_,
    Float64_,
    Int8_,
    Int16_,
    Int32_,
    Int64_,
    UInt8_,
    UInt16_,
    UInt32_,
    UInt64_,
)


class RawMessageModel(BaseModel):
    value: Any


class RawMessage(Message):
    payload: RawMessageModel

    def __setattr__(self, name: str, value: Any) -> None:
        # Backwards compatibility for 'value' of V2 raw messages
        if name == "value":
            self.payload.value = value
            return
        super().__setattr__(name, value)

    @property
    def value(self) -> Any:
        return self.payload.value


class BooleanModel(RawMessageModel):
    value: bool = Field(False, description="The raw boolean value.")


class Boolean(RawMessage):
    """A raw boolean."""

    _TYPE = KMessageTypeData("object", "raw.boolean")

    payload: BooleanModel = BooleanModel()


class TextModel(RawMessageModel):
    value: str = Field("", description="The raw string value.")


class Text(RawMessage):
    """A raw string."""

    _TYPE = KMessageTypeData("object", "raw.text")

    payload: TextModel = TextModel()


class Float32Model(RawMessageModel):
    value: Float32_ = Field(0.0, description="The raw 32-bit floating point value.")


class Float32(RawMessage):
    """A raw 32-bit floating point."""

    _TYPE = KMessageTypeData("object", "raw.float32")

    payload: Float32Model = Float32Model()


class Float64Model(RawMessageModel):
    value: Float64_ = Field(0.0, description="The raw 64-bit floating point value.")


class Float64(RawMessage):
    """A raw 64-bit floating point."""

    _TYPE = KMessageTypeData("object", "raw.float64")

    payload: Float64Model = Float64Model()


class Int8Model(RawMessageModel):
    value: Int8_ = Field(0, description="The raw signed 8-bit integer value.")


class Int8(RawMessage):
    """A raw signed 8-bit integer."""

    _TYPE = KMessageTypeData("object", "raw.int8")

    payload: Int8Model = Int8Model()


class Int16Model(RawMessageModel):
    value: Int16_ = Field(0, description="The raw signed 16-bit integer value.")


class Int16(RawMessage):
    """A raw signed 16-bit integer."""

    _TYPE = KMessageTypeData("object", "raw.int16")

    payload: Int16Model = Int16Model()


class Int32Model(RawMessageModel):
    value: Int32_ = Field(0, description="The raw signed 32-bit integer value.")


class Int32(RawMessage):
    """A raw signed 32-bit integer."""

    _TYPE = KMessageTypeData("object", "raw.int32")

    payload: Int32Model = Int32Model()


class Int64Model(RawMessageModel):
    value: Int64_ = Field(0, description="The raw signed 64-bit integer value.")


class Int64(RawMessage):
    """A raw signed 64-bit integer."""

    _TYPE = KMessageTypeData("object", "raw.int64")

    payload: Int64Model = Int64Model()


class UInt8Model(RawMessageModel):
    value: UInt8_ = Field(0, description="The raw unsigned 8-bit integer value.")


class UInt8(RawMessage):
    """A raw unsigned 8-bit integer."""

    _TYPE = KMessageTypeData("object", "raw.uint8")

    payload: UInt8Model = UInt8Model()


class UInt16Model(RawMessageModel):
    value: UInt16_ = Field(0, description="The raw unsigned 16-bit integer value.")


class UInt16(RawMessage):
    """A raw unsigned 16-bit integer."""

    _TYPE = KMessageTypeData("object", "raw.uint16")

    payload: UInt16Model = UInt16Model()


class UInt32Model(RawMessageModel):
    value: UInt32_ = Field(0, description="The raw unsigned 32-bit integer value.")


class UInt32(RawMessage):
    """A raw unsigned 32-bit integer."""

    _TYPE = KMessageTypeData("object", "raw.uint32")

    payload: UInt32Model = UInt32Model()


class UInt64Model(RawMessageModel):
    value: UInt64_ = Field(0, description="The raw unsigned 64-bit integer value.")


class UInt64(RawMessage):
    """A raw unsigned 64-bit integer."""

    _TYPE = KMessageTypeData("object", "raw.uint64")

    payload: UInt64Model = UInt64Model()


class ControlChangeModel(BaseModel):
    timeout: Optional[int] = Field(None, description="Timeout for retries")
    retries: Optional[int] = Field(None, description="Max retries")
    expiration_date: datetime = Field(description="Absolutc expiration Date in UTC")
    payload: Any = Field(None, description="Control Change payload")

    class Config:
        json_encoders = {datetime: to_rfc3339_timestamp}

    @validator('expiration_date', pre=True, always=True)
    def parse_expiration_date(cls, v: Union[str, datetime]) -> datetime:
        if isinstance(v, str):
            return from_rfc3339_timestamp(v)
        return v


class ControlChange(Message):
    """Generic Control Change Message"""

    _TYPE = KMessageTypeControl(icd="kelvin.control_change")

    payload: ControlChangeModel


class StateEnum(str, Enum):
    ready = "ready"
    sent = "sent"
    failed = "failed"
    processed = "processed"
    applied = "applied"


class ControlChangeStatusModel(BaseModel):
    state: StateEnum
    message: Optional[str] = Field(description="")
    payload: Any = Field(None, description="Metric value at status time")


class ControlChangeStatus(Message):
    """Generic Control Change Message"""

    _TYPE = KMessageTypeControlStatus(icd="kelvin.control_change_status")

    payload: ControlChangeStatusModel


class SensorDataModel(BaseModel):
    data: List[Float64_] = Field(..., description="Array of sensor measurements.", min_items=1)
    sample_rate: float = Field(..., description="Sensor sample-rate in Hertz.", gt=0.0)


class SensorData(Message):
    """Sensor data."""

    _TYPE = KMessageTypeData("object", "kelvin.sensor_data")

    payload: SensorDataModel


class RecommendationControlChangeModel(ControlChangeModel):
    retries: Optional[int] = Field(None, description="Max retries", alias="retry")
    resource: KRN
    control_change_id: Optional[str] = Field(None, description="Control Change ID")


class RecommendationActionsModel(BaseModel):
    control_changes: List[RecommendationControlChangeModel] = []


class RecommendationModel(BaseModel):
    source: KRN
    resource: KRN
    type: str
    description: Optional[str]
    confidence: Optional[int] = Field(ge=1, le=4)
    expiration_date: Optional[datetime]
    actions: RecommendationActionsModel = RecommendationActionsModel()
    metadata: Dict[str, Any] = {}

    class Config:
        json_encoders = {datetime: to_rfc3339_timestamp}

    @validator('expiration_date', pre=True, always=True)
    def parse_expiration_date(cls, v: Union[str, datetime]) -> datetime:
        if isinstance(v, str):
            return from_rfc3339_timestamp(v)
        return v


class Recommendation(Message):
    _TYPE = KMessageTypeRecommendation()

    payload: RecommendationModel
