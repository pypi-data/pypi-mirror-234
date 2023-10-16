from .types.v1 import datahub_pb2 as _datahub_pb2
from ...validate.v1 import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateDatahubIntegrationRequest(_message.Message):
    __slots__ = ["sync_direction", "generalized_metadata_service_url", "active", "api_key", "synced_entities"]
    SYNC_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    GENERALIZED_METADATA_SERVICE_URL_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    SYNCED_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    sync_direction: str
    generalized_metadata_service_url: str
    active: bool
    api_key: str
    synced_entities: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, sync_direction: _Optional[str] = ..., generalized_metadata_service_url: _Optional[str] = ..., active: bool = ..., api_key: _Optional[str] = ..., synced_entities: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateDatahubIntegrationResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetDatahubIntegrationRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetDatahubIntegrationResponse(_message.Message):
    __slots__ = ["integration"]
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: _datahub_pb2.Datahub
    def __init__(self, integration: _Optional[_Union[_datahub_pb2.Datahub, _Mapping]] = ...) -> None: ...

class UpdateDatahubIntegrationRequest(_message.Message):
    __slots__ = ["id", "sync_direction", "generalized_metadata_service_url", "active", "api_key", "synced_entities"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SYNC_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    GENERALIZED_METADATA_SERVICE_URL_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    SYNCED_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    id: str
    sync_direction: str
    generalized_metadata_service_url: str
    active: bool
    api_key: str
    synced_entities: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., sync_direction: _Optional[str] = ..., generalized_metadata_service_url: _Optional[str] = ..., active: bool = ..., api_key: _Optional[str] = ..., synced_entities: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateDatahubIntegrationResponse(_message.Message):
    __slots__ = ["integration"]
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: _datahub_pb2.Datahub
    def __init__(self, integration: _Optional[_Union[_datahub_pb2.Datahub, _Mapping]] = ...) -> None: ...

class RefreshWebhookTokenRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class RefreshWebhookTokenResponse(_message.Message):
    __slots__ = ["token"]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class DeleteDatahubIntegrationRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteDatahubIntegrationResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
