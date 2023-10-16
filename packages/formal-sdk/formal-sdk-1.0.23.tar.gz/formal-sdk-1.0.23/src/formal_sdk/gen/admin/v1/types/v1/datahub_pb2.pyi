from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Datahub(_message.Message):
    __slots__ = ["id", "webhook_secret", "organization_id", "name", "active", "generalized_metadata_service_url", "sync_direction", "synced_entities", "created_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_SECRET_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    GENERALIZED_METADATA_SERVICE_URL_FIELD_NUMBER: _ClassVar[int]
    SYNC_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    SYNCED_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    webhook_secret: str
    organization_id: str
    name: str
    active: bool
    generalized_metadata_service_url: str
    sync_direction: str
    synced_entities: _containers.RepeatedScalarFieldContainer[str]
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., webhook_secret: _Optional[str] = ..., organization_id: _Optional[str] = ..., name: _Optional[str] = ..., active: bool = ..., generalized_metadata_service_url: _Optional[str] = ..., sync_direction: _Optional[str] = ..., synced_entities: _Optional[_Iterable[str]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
