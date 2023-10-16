from .types.v1 import satellite_pb2 as _satellite_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateSatelliteRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class CreateSatelliteResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetSatelliteByIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetSatelliteByIdResponse(_message.Message):
    __slots__ = ["satellite"]
    SATELLITE_FIELD_NUMBER: _ClassVar[int]
    satellite: _satellite_pb2.Satellite
    def __init__(self, satellite: _Optional[_Union[_satellite_pb2.Satellite, _Mapping]] = ...) -> None: ...

class GetSatellitesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetSatellitesResponse(_message.Message):
    __slots__ = ["satellites"]
    SATELLITES_FIELD_NUMBER: _ClassVar[int]
    satellites: _containers.RepeatedCompositeFieldContainer[_satellite_pb2.Satellite]
    def __init__(self, satellites: _Optional[_Iterable[_Union[_satellite_pb2.Satellite, _Mapping]]] = ...) -> None: ...

class DeleteSatelliteRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteSatelliteResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
