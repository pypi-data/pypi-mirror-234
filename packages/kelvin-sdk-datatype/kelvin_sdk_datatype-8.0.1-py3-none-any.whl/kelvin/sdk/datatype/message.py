from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from functools import wraps
from importlib import import_module
from typing import Any, ClassVar, Dict, Optional, Type, Union, cast
from uuid import uuid4
from warnings import warn

import orjson
from pydantic import BaseModel, Field, validator

from kelvin.sdk.datatype.exception import DataTypeError
from kelvin.sdk.datatype.krn import KRN, KRNAssetDataStream, KRNAssetMetric, KRNWorkload
from kelvin.sdk.datatype.model import Model
from kelvin.sdk.datatype.msg_type import KMessageType, KMessageTypeData
from kelvin.sdk.datatype.utils import from_rfc3339_timestamp, to_rfc3339_timestamp


@dataclass
class Header:
    type: str
    name: str
    id: Optional[str]
    trace_id: Optional[str]
    source: Optional[Dict[str, str]]
    target: Optional[Dict[str, str]]
    asset_name: str
    time_of_validity: int


class Message(Model):
    _MESSAGE_TYPES: ClassVar[Dict[KMessageType, Type['Message']]] = {}
    _TYPE: ClassVar[Optional[KMessageType]] = None

    id: str = ""
    type: KMessageType
    trace_id: Optional[str] = None
    source: Optional[KRN]
    timestamp: datetime = Field(default_factory=lambda: datetime.now().astimezone())
    resource: Optional[KRN]

    payload: Any

    class Config:
        underscore_attrs_are_private = True
        json_encoders = {
            datetime: to_rfc3339_timestamp,
            KRN: KRN.encode,
            KMessageType: KMessageType.encode,
        }

    def __init_subclass__(cls) -> None:
        if cls._TYPE:
            Message._MESSAGE_TYPES[cls._TYPE] = cls

    def __new__(cls, **kwargs: Any) -> Message:  # pyright: ignore
        """Initialise message."""

        if cls._TYPE:
            MSG_T = cls
        else:
            msg_type = cls._get_msg_type_from_payload(**kwargs)
            if msg_type is None:
                raise ValueError("Missing message type") from None

            MSG_T = cls.get_type(msg_type)
        obj = super().__new__(MSG_T)
        return obj

    def __init__(self, **kwargs: Any) -> None:  # pyright: ignore
        """
        Create a kelvin Message.

        Parameters
        ----------
        id : str, optional
            UUID of the message. Optional, auto generated if not provided.
        type : KMessageType
            Message Type
        trace_id : str, optional
            Optional trace id. UUID
        source : KRN, optional
            Identifies the source of the message.
        timestamp : datetime, optional
            Sets a timestamp for the message. If not provided current time is used.
        resource : KRN, optional
            Sets a resource that the message relates to.
        payload : Any
            Payload of the message. Specific for each message sub type.
        """

        new_kwargs = kwargs
        if kwargs.get("data_type"):
            new_kwargs = self._convert_message_v1(**kwargs)
        elif kwargs.get("_"):
            new_kwargs = self._convert_message_v0(**kwargs)

        new_kwargs["type"] = self._TYPE

        super().__init__(**new_kwargs)

    @classmethod
    def get_type(cls, _type: KMessageType) -> Type[Message]:
        """Get message type by name."""
        try:
            return Message._MESSAGE_TYPES[_type]
        except KeyError:
            raise ValueError(f"Unknown message type: {repr(_type)}") from None

    @validator('id', pre=True, always=True)
    def default_id(cls, v: str) -> str:
        return v or str(uuid4())

    @validator('timestamp', pre=True, always=True)
    def default_timestamp(cls, v: Union[str, datetime]) -> datetime:
        if isinstance(v, str):
            return from_rfc3339_timestamp(v)

        return v

    @wraps(BaseModel.dict)
    def dict(
        self,
        by_alias: bool = True,
        exclude_none: bool = True,
        exclude_unset: bool = False,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Generate a dictionary representation of the model."""

        return super().dict(
            by_alias=by_alias, exclude_none=exclude_none, exclude_unset=exclude_unset, **kwargs
        )

    @wraps(BaseModel.json)
    def json(
        self,
        by_alias: bool = True,
        exclude_none: bool = True,
        exclude_unset: bool = False,
        **kwargs: Any,
    ) -> str:
        """Generate a dictionary representation of the model."""

        return super().json(
            by_alias=by_alias, exclude_none=exclude_none, exclude_unset=exclude_unset, **kwargs
        )

    def encode(self, header: bool = False) -> bytes:
        """Encode message in V1"""
        # encode as V2 if the message is not type data (only data is using V1 still)
        if not isinstance(self._TYPE, KMessageTypeData):
            return bytes(self.json(), 'utf-8')

        data_type = cast(KMessageTypeData, self.type).icd
        asset = self.resource.asset if isinstance(self.resource, KRNAssetMetric) else None
        name = self.resource.metric if isinstance(self.resource, KRNAssetMetric) else None
        source = (
            f"{self.source.node}/{self.source.workload}"
            if isinstance(self.source, KRNWorkload)
            else None
        )

        # try to catch some cases with messages not casting (improve this)
        msg_dict = {}
        try:
            msg_dict = {
                "asset_name": asset,
                "data_type": data_type,
                "id": self.id,
                "name": name,
                "source": source,
                "timestamp": to_rfc3339_timestamp(self.timestamp),  # type: ignore
                "payload": cast(Model, self.payload).dict(),
            }
        except AttributeError:
            msg_dict = {
                "type": str(self.type),
                "id": self.id,
                "trace_id": self.trace_id,
                "name": name,
                "timestamp": to_rfc3339_timestamp(self.timestamp),  # type: ignore
                "payload": self.payload,
                "source": source,
                "resource": str(self.resource) if self.resource else None,
            }

        # remove None
        msg_dict = {k: v for k, v in msg_dict.items() if v is not None}

        return orjson.dumps(msg_dict)

    @classmethod
    def decode(cls, data: bytes) -> Message:
        return cls.parse_raw(data)

    @staticmethod
    def _convert_message_v1(**kwargs: Dict) -> Dict:
        result: Dict[str, Any] = {
            "id": kwargs.get("id", None),
            "timestamp": kwargs.get("timestamp", None),
        }

        asset = kwargs.get("asset_name", None)
        metric = kwargs.get("name", None)
        if asset and metric:
            result["resource"] = f"krn:am:{asset}/{metric}"

        # result["type"] = KMessageTypeObject(icd=str(kwargs.get("data_type")))

        source = kwargs.get("source", None)
        if source:
            result["source"] = "krn:wl:" + str(source)

        result["payload"] = kwargs.get("payload")

        return result

    @staticmethod
    def _convert_message_v0(**kwargs: Dict) -> Dict:
        result: Dict[str, Any] = {}

        header = kwargs.pop("_")

        asset = header.get("asset_name", None) or ""
        metric = header.get("name", None) or ""
        # resource should not have empty asset but kelvin-app uses v0 messages with no asset
        result["resource"] = KRNAssetMetric(asset, metric)

        result["type"] = "data;icd=" + str(header.get("data_type"))

        source = header.get("source", None)
        if source:
            if isinstance(source, dict):
                source = source.get("node_name", "") + "/" + source.get("workload_name", "")
            result["source"] = "krn:wl:" + source

        timestamp_ns = header.get("time_of_validity", None)
        if timestamp_ns is not None:
            result["timestamp"] = datetime.fromtimestamp(timestamp_ns / 1e9).astimezone()

        id = timestamp_ns = header.get("id", None)
        if id:
            result["id"] = id

        # the remaining kwargs are payload
        result["payload"] = kwargs

        return result

    @staticmethod
    def _get_msg_type_from_payload(**kwargs: Any) -> Optional[KMessageType]:
        # "type" from v2 or "data_type" from v1 or "_.type" from v0
        v2_type = str(kwargs.get("type", ""))
        if v2_type:
            return KMessageType.from_string(v2_type)

        icd = kwargs.get("data_type") or kwargs.get("_", {}).get("type")
        if icd:
            return KMessageTypeData(primitive="object", icd=icd)

        return None

    @classmethod
    def make_message(
        cls: Type[Message],
        _type: str,
        _name: Optional[str] = None,
        _time_of_validity: Optional[Union[int, float]] = None,
        _source: Optional[Union[str, Dict[str, str]]] = None,
        _target: Optional[str] = None,
        _asset_name: Optional[str] = None,
        _id: Optional[str] = None,
        _trace_id: Optional[str] = None,
        **kwargs: Any,
    ) -> Message:
        """
        Create a message object.

        Parameters
        ----------
        _type : str, optional
            Message type (e.g. ``float32``, ``kelvin.beam_pump``)
        _name : str, optional
            Message name
        _time_of_validity : int, optional
            Time of validity in nano-seconds
        _source : dict, optional
            Message source
        _target : dict, optional
            Message target
        _asset_name : str, optional
            Asset name
        **kwargs :
            Additional properties for message (e.g. ``value`` for raw types)

        """

        _ = {
            "type": _type,
            "name": _name or None,
            "time_of_validity": _time_of_validity,
            "source": _source or None,
            "target": _target or None,
            "asset_name": _asset_name or None,
            "id": _id or None,
            "trace_id": _trace_id or None,
        }

        return cls(_=_, **kwargs)

    def _fill_header(self) -> Header:
        data_type = self.type.icd if isinstance(self.type, KMessageTypeData) else self.type.msg_type
        if data_type is None:
            raise DataTypeError(f"Cannot encode icd {data_type} in V1 version.")

        asset = ""
        name = ""
        if isinstance(self.resource, KRNAssetMetric):
            asset = self.resource.asset
            name = self.resource.metric
        if isinstance(self.resource, KRNAssetDataStream):
            asset = self.resource.asset
            name = self.resource.data_stream

        if isinstance(self.source, KRNWorkload):
            source: Optional[Dict[str, str]] = {
                "node_name": self.source.node,
                "workload_name": self.source.workload,
            }
        else:
            source = None

        return Header(
            type=data_type,
            name=name,
            id=self.id,
            trace_id=self.trace_id,
            source=source,
            target=None,
            asset_name=asset,
            time_of_validity=int(self.timestamp.timestamp() * 1e9),  # type: ignore
        )

    # header backwards compatiblity
    @property
    def _(self) -> Header:
        warn("Header property is being deprecated, use msg V2 equivalent", DeprecationWarning)
        return self._fill_header()

    @property
    def header(self) -> Header:
        warn("Header property is being deprecated, use msg V2 equivalent", DeprecationWarning)
        return self._fill_header()


make_message = Message.make_message
