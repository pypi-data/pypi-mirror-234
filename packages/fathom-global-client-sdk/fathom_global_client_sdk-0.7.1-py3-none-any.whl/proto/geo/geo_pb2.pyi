from validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Point(_message.Message):
    __slots__ = ["longitude", "latitude"]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    longitude: float
    latitude: float
    def __init__(self, longitude: _Optional[float] = ..., latitude: _Optional[float] = ...) -> None: ...

class MultiPoint(_message.Message):
    __slots__ = ["points"]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[Point]
    def __init__(self, points: _Optional[_Iterable[_Union[Point, _Mapping]]] = ...) -> None: ...

class LineString(_message.Message):
    __slots__ = ["points"]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[Point]
    def __init__(self, points: _Optional[_Iterable[_Union[Point, _Mapping]]] = ...) -> None: ...

class Polygon(_message.Message):
    __slots__ = ["lines"]
    LINES_FIELD_NUMBER: _ClassVar[int]
    lines: _containers.RepeatedCompositeFieldContainer[LineString]
    def __init__(self, lines: _Optional[_Iterable[_Union[LineString, _Mapping]]] = ...) -> None: ...
