from .types.v1 import connection_pb2 as _connection_pb2
from .types.v1 import organization_pb2 as _organization_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetWorkOsOrgRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetWorkOsOrgResponse(_message.Message):
    __slots__ = ["workos_org", "self_sign_up"]
    WORKOS_ORG_FIELD_NUMBER: _ClassVar[int]
    SELF_SIGN_UP_FIELD_NUMBER: _ClassVar[int]
    workos_org: _organization_pb2.Organization
    self_sign_up: bool
    def __init__(self, workos_org: _Optional[_Union[_organization_pb2.Organization, _Mapping]] = ..., self_sign_up: bool = ...) -> None: ...

class UpdateWorkOsOrgRequest(_message.Message):
    __slots__ = ["domains", "self_sign_up"]
    DOMAINS_FIELD_NUMBER: _ClassVar[int]
    SELF_SIGN_UP_FIELD_NUMBER: _ClassVar[int]
    domains: _containers.RepeatedScalarFieldContainer[str]
    self_sign_up: bool
    def __init__(self, domains: _Optional[_Iterable[str]] = ..., self_sign_up: bool = ...) -> None: ...

class UpdateWorkOsOrgResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetSsoConnectionsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetSsoConnectionsResponse(_message.Message):
    __slots__ = ["connections"]
    CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    connections: _containers.RepeatedCompositeFieldContainer[_connection_pb2.Connection]
    def __init__(self, connections: _Optional[_Iterable[_Union[_connection_pb2.Connection, _Mapping]]] = ...) -> None: ...

class DeleteConnectionRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteConnectionResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
