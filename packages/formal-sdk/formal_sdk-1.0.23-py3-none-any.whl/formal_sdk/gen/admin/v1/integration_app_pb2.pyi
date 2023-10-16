from .types.v1 import app_pb2 as _app_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RefreshIntegrationAppsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class RefreshIntegrationAppsResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetIntegrationAppsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetIntegrationAppsResponse(_message.Message):
    __slots__ = ["integrations"]
    INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    integrations: _containers.RepeatedCompositeFieldContainer[_app_pb2.IntegrationApp]
    def __init__(self, integrations: _Optional[_Iterable[_Union[_app_pb2.IntegrationApp, _Mapping]]] = ...) -> None: ...

class GetIntegrationByIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetIntegrationByIdResponse(_message.Message):
    __slots__ = ["integration"]
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: _app_pb2.IntegrationApp
    def __init__(self, integration: _Optional[_Union[_app_pb2.IntegrationApp, _Mapping]] = ...) -> None: ...

class CreateIntegrationAppRequest(_message.Message):
    __slots__ = ["name", "type", "metabase_hostname", "metabase_username", "metabase_password", "linked_db_user_id", "fivetran_api_key", "fivetran_api_secret"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    METABASE_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    METABASE_USERNAME_FIELD_NUMBER: _ClassVar[int]
    METABASE_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    LINKED_DB_USER_ID_FIELD_NUMBER: _ClassVar[int]
    FIVETRAN_API_KEY_FIELD_NUMBER: _ClassVar[int]
    FIVETRAN_API_SECRET_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: str
    metabase_hostname: str
    metabase_username: str
    metabase_password: str
    linked_db_user_id: str
    fivetran_api_key: str
    fivetran_api_secret: str
    def __init__(self, name: _Optional[str] = ..., type: _Optional[str] = ..., metabase_hostname: _Optional[str] = ..., metabase_username: _Optional[str] = ..., metabase_password: _Optional[str] = ..., linked_db_user_id: _Optional[str] = ..., fivetran_api_key: _Optional[str] = ..., fivetran_api_secret: _Optional[str] = ...) -> None: ...

class CreateIntegrationAppResponse(_message.Message):
    __slots__ = ["integration"]
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: _app_pb2.IntegrationApp
    def __init__(self, integration: _Optional[_Union[_app_pb2.IntegrationApp, _Mapping]] = ...) -> None: ...

class DeleteIntegrationAppRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteIntegrationAppResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
