from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Domain(_message.Message):
    __slots__ = ["id", "name", "description", "owners", "excluded_paths", "included_paths"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OWNERS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_PATHS_FIELD_NUMBER: _ClassVar[int]
    INCLUDED_PATHS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    owners: _containers.RepeatedCompositeFieldContainer[Owner]
    excluded_paths: _containers.RepeatedScalarFieldContainer[str]
    included_paths: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., owners: _Optional[_Iterable[_Union[Owner, _Mapping]]] = ..., excluded_paths: _Optional[_Iterable[str]] = ..., included_paths: _Optional[_Iterable[str]] = ...) -> None: ...

class Owner(_message.Message):
    __slots__ = ["object_type", "object_id"]
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    object_type: str
    object_id: str
    def __init__(self, object_type: _Optional[str] = ..., object_id: _Optional[str] = ...) -> None: ...
