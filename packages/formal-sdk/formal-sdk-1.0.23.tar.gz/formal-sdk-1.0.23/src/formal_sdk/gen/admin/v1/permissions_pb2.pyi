from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetPermissionsByServiceRequest(_message.Message):
    __slots__ = ["service"]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    service: str
    def __init__(self, service: _Optional[str] = ...) -> None: ...

class GetPermissionsByServiceResponse(_message.Message):
    __slots__ = ["permissions"]
    class PermissionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bool
        def __init__(self, key: _Optional[str] = ..., value: bool = ...) -> None: ...
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    permissions: _containers.ScalarMap[str, bool]
    def __init__(self, permissions: _Optional[_Mapping[str, bool]] = ...) -> None: ...

class GetPermissionsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetPermissionsResponse(_message.Message):
    __slots__ = ["permissions"]
    class PermissionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bool
        def __init__(self, key: _Optional[str] = ..., value: bool = ...) -> None: ...
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    permissions: _containers.ScalarMap[str, bool]
    def __init__(self, permissions: _Optional[_Mapping[str, bool]] = ...) -> None: ...
