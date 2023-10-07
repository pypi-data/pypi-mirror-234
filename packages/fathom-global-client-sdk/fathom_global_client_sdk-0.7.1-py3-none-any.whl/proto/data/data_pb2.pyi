from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class Resolution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    RESOLUTION_UNSPECIFIED: _ClassVar[Resolution]
    RESOLUTION_1_ARC_SEC: _ClassVar[Resolution]
    RESOLUTION_THIRD_ARC_SEC: _ClassVar[Resolution]
RESOLUTION_UNSPECIFIED: Resolution
RESOLUTION_1_ARC_SEC: Resolution
RESOLUTION_THIRD_ARC_SEC: Resolution
