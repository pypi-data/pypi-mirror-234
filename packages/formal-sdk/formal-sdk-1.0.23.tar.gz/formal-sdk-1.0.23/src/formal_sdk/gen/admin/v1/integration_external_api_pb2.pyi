from ...validate.v1 import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Auth(_message.Message):
    __slots__ = ["type", "basic"]
    class Basic(_message.Message):
        __slots__ = ["username", "password"]
        USERNAME_FIELD_NUMBER: _ClassVar[int]
        PASSWORD_FIELD_NUMBER: _ClassVar[int]
        username: str
        password: str
        def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...
    TYPE_FIELD_NUMBER: _ClassVar[int]
    BASIC_FIELD_NUMBER: _ClassVar[int]
    type: str
    basic: Auth.Basic
    def __init__(self, type: _Optional[str] = ..., basic: _Optional[_Union[Auth.Basic, _Mapping]] = ...) -> None: ...

class CreateExternalApiIntegrationRequest(_message.Message):
    __slots__ = ["type", "name", "url", "auth"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    AUTH_FIELD_NUMBER: _ClassVar[int]
    type: str
    name: str
    url: str
    auth: Auth
    def __init__(self, type: _Optional[str] = ..., name: _Optional[str] = ..., url: _Optional[str] = ..., auth: _Optional[_Union[Auth, _Mapping]] = ...) -> None: ...

class CreateExternalApiIntegrationResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ApiIntegration(_message.Message):
    __slots__ = ["id", "type", "name", "url", "auth_type", "created_at", "updated_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    AUTH_TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    name: str
    url: str
    auth_type: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ..., name: _Optional[str] = ..., url: _Optional[str] = ..., auth_type: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetExternalApiIntegrationRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetExternalApiIntegrationResponse(_message.Message):
    __slots__ = ["integration"]
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: ApiIntegration
    def __init__(self, integration: _Optional[_Union[ApiIntegration, _Mapping]] = ...) -> None: ...

class DeleteExternalApiIntegrationRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteExternalApiIntegrationResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetExternalApiIntegrationsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetExternalApiIntegrationsResponse(_message.Message):
    __slots__ = ["integrations"]
    INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    integrations: _containers.RepeatedCompositeFieldContainer[ApiIntegration]
    def __init__(self, integrations: _Optional[_Iterable[_Union[ApiIntegration, _Mapping]]] = ...) -> None: ...
