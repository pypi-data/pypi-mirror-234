from __future__ import annotations

from typing import Any, Callable, Dict, Generator, Optional, Type


class KRN:
    """Kelvin Resource Name representation"""

    _KRN_TYPES: Dict[str, Type[KRN]] = {}
    _NS_ID: Optional[str] = None

    ns_id: str
    ns_string: str

    def __init_subclass__(cls) -> None:
        if cls._NS_ID:
            KRN._KRN_TYPES[cls._NS_ID] = cls

    def __init__(self, ns_id: str, ns_string: str) -> None:
        self.ns_id = ns_id
        self.ns_string = ns_string

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> KRN:
        if isinstance(v, str):
            return cls.from_string(v)

        if isinstance(v, KRN):
            return v

        raise TypeError('Invalid type for KRN. KRN or string required.')

    @classmethod
    def from_krn(cls, ns_id: str, ns_string: str) -> KRN:
        return cls(ns_id, ns_string)

    @classmethod
    def from_string(cls, v: str) -> KRN:
        try:
            krn, ns_id, ns_string = v.split(":", 2)
        except ValueError:
            raise ValueError("expected format 'krn:<nid>:<nss>'")

        if krn != "krn":
            raise ValueError("expected start by 'krn'")

        T = KRN._KRN_TYPES.get(ns_id, KRN)
        return T.from_krn(ns_id, ns_string)

    def __eq__(self, other: Any) -> bool:
        if type(self) != type(other):
            return False

        return self.ns_id == other.ns_id and self.ns_string == other.ns_string

    def __hash__(self) -> int:
        return hash((self.ns_id, self.ns_string))

    def __str__(self) -> str:
        return f"krn:{self.ns_id}:{self.ns_string}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({str(self)})"

    def encode(self) -> str:
        return str(self)


class KRNAsset(KRN):
    _NS_ID: str = "asset"
    """Kelvin Resource Name Asset Metric"""
    asset: str

    def __init__(self, asset: str) -> None:
        super().__init__(self._NS_ID, asset)
        self.asset = asset

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(asset='{self.asset}')"

    @classmethod
    def from_krn(cls, ns_id: str, ns_string: str) -> KRNAsset:
        if ns_id != cls._NS_ID:
            raise ValueError(f"Error parsing {cls.__name__}. Expected {cls._NS_ID}, got {ns_id}")

        return cls(ns_string)


class KRNAssetMetric(KRN):
    _NS_ID: str = "am"
    """Kelvin Resource Name Asset"""
    asset: str
    metric: str

    def __init__(self, asset: str, metric: str) -> None:
        super().__init__(self._NS_ID, asset + "/" + metric)
        self.asset = asset
        self.metric = metric

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(asset='{self.asset}', metric='{self.metric}')"

    @classmethod
    def from_krn(cls, ns_id: str, ns_string: str) -> KRNAssetMetric:
        if ns_id != cls._NS_ID:
            raise ValueError(f"Error parsing {cls.__name__}. Expected {cls._NS_ID}, got {ns_id}")

        try:
            asset, metric = ns_string.split("/", 1)
        except ValueError:
            raise ValueError("expected format 'krn:am:<asset>/<metric>'")

        return cls(asset, metric)


class KRNAssetDataStream(KRN):
    _NS_ID: str = "ad"
    """Kelvin Resource Name Asset DataStream"""
    asset: str
    data_stream: str

    def __init__(self, asset: str, data_stream: str) -> None:
        super().__init__(self._NS_ID, asset + "/" + data_stream)
        self.asset = asset
        self.data_stream = data_stream

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(asset='{self.asset}', data_stream='{self.data_stream}')"

    @classmethod
    def from_krn(cls, ns_id: str, ns_string: str) -> KRNAssetDataStream:
        if ns_id != cls._NS_ID:
            raise ValueError(f"Error parsing {cls.__name__}. Expected {cls._NS_ID}, got {ns_id}")

        try:
            asset, data_stream = ns_string.split("/", 1)
        except ValueError:
            raise ValueError("expected format 'krn:am:<asset>/<data_stream>'")

        return cls(asset, data_stream)


class KRNAssetParameter(KRN):
    _NS_ID: str = "ap"
    """Kelvin Resource Name Asset Parameter"""
    asset: str
    parameter: str

    def __init__(self, asset: str, parameter: str) -> None:
        super().__init__(self._NS_ID, asset + "/" + parameter)
        self.asset = asset
        self.parameter = parameter

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(asset='{self.asset}', parameter='{self.parameter}')"

    @classmethod
    def from_krn(cls, ns_id: str, ns_string: str) -> KRNAssetParameter:
        if ns_id != cls._NS_ID:
            raise ValueError(f"Error parsing {cls.__name__}. Expected {cls._NS_ID}, got {ns_id}")

        try:
            asset, parameter = ns_string.split("/", 1)
        except ValueError:
            raise ValueError("expected format 'krn:am:<asset>/<parameter>'")

        return cls(asset, parameter)


class KRNParameter(KRN):
    _NS_ID: str = "param"
    """Kelvin Resource Name Parameter"""
    parameter: str

    def __init__(self, parameter: str) -> None:
        super().__init__(self._NS_ID, parameter)
        self.parameter = parameter

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(parameter='{self.parameter}')"

    @classmethod
    def from_krn(cls, ns_id: str, ns_string: str) -> KRNParameter:
        if ns_id != cls._NS_ID:
            raise ValueError(f"Error parsing {cls.__name__}. Expected {cls._NS_ID}, got {ns_id}")

        return cls(ns_string)


class KRNWorkload(KRN):
    _NS_ID: str = "wl"
    """Kelvin Resource Name Workload"""
    node: str
    workload: str

    def __init__(self, node: str, workload: str) -> None:
        super().__init__(self._NS_ID, node + "/" + workload)
        self.node = node
        self.workload = workload

    @property
    def node_name(self) -> str:
        "Backwards compatibility"
        return self.node

    @property
    def workload_name(self) -> str:
        "Backwards compatibility"
        return self.workload

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(node='{self.node}', workload='{self.workload}')"

    @classmethod
    def from_krn(cls, ns_id: str, ns_string: str) -> KRNWorkload:
        if ns_id != cls._NS_ID:
            raise ValueError(f"Error parsing {cls.__name__}. Expected {cls._NS_ID}, got {ns_id}")

        try:
            node, workload = ns_string.split("/", 1)
        except ValueError:
            raise ValueError("expected format 'krn:wl:<node>/<workload>'")

        return cls(node, workload)


class KRNWorkloadApp(KRN):
    _NS_ID: str = "wlapp"
    """Kelvin Resource Name Workload App"""
    node: str
    workload: str
    app: str

    def __init__(self, node: str, workload: str, app: str) -> None:
        super().__init__(self._NS_ID, node + "/" + workload + ":" + app)
        self.node = node
        self.workload = workload
        self.app = app

    @property
    def node_name(self) -> str:
        "Backwards compatibility"
        return self.node

    @property
    def workload_name(self) -> str:
        "Backwards compatibility"
        return self.workload

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(node='{self.node}', workload='{self.workload}', app='{self.app}')"

    @classmethod
    def from_krn(cls, ns_id: str, ns_string: str) -> KRNWorkloadApp:
        if ns_id != cls._NS_ID:
            raise ValueError(f"Error parsing {cls.__name__}. Expected {cls._NS_ID}, got {ns_id}")

        try:
            node_workload, app = ns_string.split(":", 1)
            node, workload = node_workload.split("/", 1)
        except ValueError:
            raise ValueError("expected format 'krn:wl:<node>/<workload>'")

        return cls(node, workload, app)


class KRNRecommendation(KRN):
    _NS_ID: str = "recommendation"
    """Kelvin Resource Name Recommendation"""
    recommendation_id: str

    def __init__(self, recommendation_id: str) -> None:
        super().__init__(self._NS_ID, recommendation_id)
        self.recommendation_id = recommendation_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(recommendation_id='{self.recommendation_id}')"

    @classmethod
    def from_krn(cls, ns_id: str, ns_string: str) -> KRNRecommendation:
        if ns_id != cls._NS_ID:
            raise ValueError(f"Error parsing {cls.__name__}. Expected {cls._NS_ID}, got {ns_id}")

        return cls(ns_string)
