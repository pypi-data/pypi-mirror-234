from .types.v1 import incident_account_pb2 as _incident_account_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeleteIncidentAccountByIdRequest(_message.Message):
    __slots__ = ["account_id"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    def __init__(self, account_id: _Optional[str] = ...) -> None: ...

class DeleteIncidentAccountByIdResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ConnectIncidentAccountRequest(_message.Message):
    __slots__ = ["name", "type", "logo", "api_key"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LOGO_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: str
    logo: str
    api_key: str
    def __init__(self, name: _Optional[str] = ..., type: _Optional[str] = ..., logo: _Optional[str] = ..., api_key: _Optional[str] = ...) -> None: ...

class ConnectIncidentAccountResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetIncidentAccountsRequest(_message.Message):
    __slots__ = ["limit", "cursor", "go_back"]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    GO_BACK_FIELD_NUMBER: _ClassVar[int]
    limit: str
    cursor: str
    go_back: bool
    def __init__(self, limit: _Optional[str] = ..., cursor: _Optional[str] = ..., go_back: bool = ...) -> None: ...

class GetIncidentAccountsResponse(_message.Message):
    __slots__ = ["accounts", "last_evaluated_key", "has_more"]
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    LAST_EVALUATED_KEY_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedCompositeFieldContainer[_incident_account_pb2.IncidentAccount]
    last_evaluated_key: str
    has_more: bool
    def __init__(self, accounts: _Optional[_Iterable[_Union[_incident_account_pb2.IncidentAccount, _Mapping]]] = ..., last_evaluated_key: _Optional[str] = ..., has_more: bool = ...) -> None: ...

class GetIncidentAccountByIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetIncidentAccountByIdResponse(_message.Message):
    __slots__ = ["account"]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    account: _incident_account_pb2.IncidentAccount
    def __init__(self, account: _Optional[_Union[_incident_account_pb2.IncidentAccount, _Mapping]] = ...) -> None: ...
