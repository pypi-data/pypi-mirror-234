from google.api import annotations_pb2 as _annotations_pb2
from proto.data import data_pb2 as _data_pb2
from proto.geo import geo_pb2 as _geo_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Code(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    UNSPECIFIED: _ClassVar[Code]
    NO_DATA: _ClassVar[Code]
    PERMANENT_WATER: _ClassVar[Code]
UNSPECIFIED: Code
NO_DATA: Code
PERMANENT_WATER: Code

class PolygonStats(_message.Message):
    __slots__ = ["mean", "min", "max", "stddev"]
    MEAN_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    STDDEV_FIELD_NUMBER: _ClassVar[int]
    mean: int
    min: int
    max: int
    stddev: int
    def __init__(self, mean: _Optional[int] = ..., min: _Optional[int] = ..., max: _Optional[int] = ..., stddev: _Optional[int] = ...) -> None: ...

class GetPolygonStatsRequest(_message.Message):
    __slots__ = ["polygon", "layers", "metadata"]
    class MetadataEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    POLYGON_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    polygon: _geo_pb2.Polygon
    layers: Layers
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, polygon: _Optional[_Union[_geo_pb2.Polygon, _Mapping]] = ..., layers: _Optional[_Union[Layers, _Mapping]] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class GetPolygonStatsResponse(_message.Message):
    __slots__ = ["stats"]
    class StatsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: PolygonStats
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[PolygonStats, _Mapping]] = ...) -> None: ...
    STATS_FIELD_NUMBER: _ClassVar[int]
    stats: _containers.MessageMap[str, PolygonStats]
    def __init__(self, stats: _Optional[_Mapping[str, PolygonStats]] = ...) -> None: ...

class GetDataRequest(_message.Message):
    __slots__ = ["polygon", "points", "shp_file", "layers", "metadata"]
    class MetadataEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    POLYGON_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    SHP_FILE_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    polygon: _geo_pb2.Polygon
    points: _geo_pb2.MultiPoint
    shp_file: bytes
    layers: Layers
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, polygon: _Optional[_Union[_geo_pb2.Polygon, _Mapping]] = ..., points: _Optional[_Union[_geo_pb2.MultiPoint, _Mapping]] = ..., shp_file: _Optional[bytes] = ..., layers: _Optional[_Union[Layers, _Mapping]] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Layers(_message.Message):
    __slots__ = ["layer_ids"]
    class Identifiers(_message.Message):
        __slots__ = ["ids"]
        IDS_FIELD_NUMBER: _ClassVar[int]
        ids: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...
    LAYER_IDS_FIELD_NUMBER: _ClassVar[int]
    layer_ids: Layers.Identifiers
    def __init__(self, layer_ids: _Optional[_Union[Layers.Identifiers, _Mapping]] = ...) -> None: ...

class GetDataResponse(_message.Message):
    __slots__ = ["results"]
    class ResultsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Data
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Data, _Mapping]] = ...) -> None: ...
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.MessageMap[str, Data]
    def __init__(self, results: _Optional[_Mapping[str, Data]] = ...) -> None: ...

class Data(_message.Message):
    __slots__ = ["resolution", "values", "polygons", "code"]
    class Value(_message.Message):
        __slots__ = ["sw_corner", "query_point", "val", "code"]
        SW_CORNER_FIELD_NUMBER: _ClassVar[int]
        QUERY_POINT_FIELD_NUMBER: _ClassVar[int]
        VAL_FIELD_NUMBER: _ClassVar[int]
        CODE_FIELD_NUMBER: _ClassVar[int]
        sw_corner: _geo_pb2.Point
        query_point: _geo_pb2.Point
        val: int
        code: Code
        def __init__(self, sw_corner: _Optional[_Union[_geo_pb2.Point, _Mapping]] = ..., query_point: _Optional[_Union[_geo_pb2.Point, _Mapping]] = ..., val: _Optional[int] = ..., code: _Optional[_Union[Code, str]] = ...) -> None: ...
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    POLYGONS_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    resolution: _data_pb2.Resolution
    values: _containers.RepeatedCompositeFieldContainer[Data.Value]
    polygons: Polygons
    code: Code
    def __init__(self, resolution: _Optional[_Union[_data_pb2.Resolution, str]] = ..., values: _Optional[_Iterable[_Union[Data.Value, _Mapping]]] = ..., polygons: _Optional[_Union[Polygons, _Mapping]] = ..., code: _Optional[_Union[Code, str]] = ...) -> None: ...

class Polygons(_message.Message):
    __slots__ = ["geo_tiffs"]
    GEO_TIFFS_FIELD_NUMBER: _ClassVar[int]
    geo_tiffs: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, geo_tiffs: _Optional[_Iterable[bytes]] = ...) -> None: ...

class CreateAccessTokenRequest(_message.Message):
    __slots__ = ["client_id", "client_secret"]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ...) -> None: ...

class CreateAccessTokenResponse(_message.Message):
    __slots__ = ["access_token", "expire_secs"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_SECS_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    expire_secs: int
    def __init__(self, access_token: _Optional[str] = ..., expire_secs: _Optional[int] = ...) -> None: ...
