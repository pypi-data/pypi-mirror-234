from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchUser(_message.Message):
    __slots__ = ["id", "db_username", "created_at", "active", "type", "status", "expire_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    DB_USERNAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    db_username: str
    created_at: _timestamp_pb2.Timestamp
    active: bool
    type: str
    status: str
    expire_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., db_username: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., active: bool = ..., type: _Optional[str] = ..., status: _Optional[str] = ..., expire_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class SearchGroup(_message.Message):
    __slots__ = ["id", "name", "description", "status", "created_at", "active"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    status: str
    created_at: _timestamp_pb2.Timestamp
    active: bool
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., status: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., active: bool = ...) -> None: ...

class SearchPolicy(_message.Message):
    __slots__ = ["id", "name", "description", "status", "created_by", "created_at", "updated_at", "active"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    status: str
    created_by: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    active: bool
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., status: _Optional[str] = ..., created_by: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., active: bool = ...) -> None: ...

class SearchDatastore(_message.Message):
    __slots__ = ["id", "datastore_id", "name", "hostname", "technology", "created_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    TECHNOLOGY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    datastore_id: str
    name: str
    hostname: str
    technology: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., datastore_id: _Optional[str] = ..., name: _Optional[str] = ..., hostname: _Optional[str] = ..., technology: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class SearchSidecar(_message.Message):
    __slots__ = ["id", "datastore_id", "name", "formal_hostname", "cloud_provider", "cloud_region", "deployment_type", "fail_open", "technology", "proxy_status", "server_connection_status", "created_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FORMAL_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    CLOUD_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    CLOUD_REGION_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    FAIL_OPEN_FIELD_NUMBER: _ClassVar[int]
    TECHNOLOGY_FIELD_NUMBER: _ClassVar[int]
    PROXY_STATUS_FIELD_NUMBER: _ClassVar[int]
    SERVER_CONNECTION_STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    datastore_id: str
    name: str
    formal_hostname: str
    cloud_provider: str
    cloud_region: str
    deployment_type: str
    fail_open: bool
    technology: str
    proxy_status: str
    server_connection_status: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., datastore_id: _Optional[str] = ..., name: _Optional[str] = ..., formal_hostname: _Optional[str] = ..., cloud_provider: _Optional[str] = ..., cloud_region: _Optional[str] = ..., deployment_type: _Optional[str] = ..., fail_open: bool = ..., technology: _Optional[str] = ..., proxy_status: _Optional[str] = ..., server_connection_status: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class SearchInventory(_message.Message):
    __slots__ = ["created_at", "updated_at", "datastore_id", "datastore_name", "path", "table_physical_id", "table_attribute_number", "name", "alias", "table_path", "data_label", "data_type", "data_type_oid", "data_label_locked_for_sidecar", "tags", "encrypted", "data_labels"]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    TABLE_PHYSICAL_ID_FIELD_NUMBER: _ClassVar[int]
    TABLE_ATTRIBUTE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ALIAS_FIELD_NUMBER: _ClassVar[int]
    TABLE_PATH_FIELD_NUMBER: _ClassVar[int]
    DATA_LABEL_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_OID_FIELD_NUMBER: _ClassVar[int]
    DATA_LABEL_LOCKED_FOR_SIDECAR_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTED_FIELD_NUMBER: _ClassVar[int]
    DATA_LABELS_FIELD_NUMBER: _ClassVar[int]
    created_at: int
    updated_at: int
    datastore_id: str
    datastore_name: str
    path: str
    table_physical_id: str
    table_attribute_number: int
    name: str
    alias: str
    table_path: str
    data_label: str
    data_type: str
    data_type_oid: int
    data_label_locked_for_sidecar: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    encrypted: bool
    data_labels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, created_at: _Optional[int] = ..., updated_at: _Optional[int] = ..., datastore_id: _Optional[str] = ..., datastore_name: _Optional[str] = ..., path: _Optional[str] = ..., table_physical_id: _Optional[str] = ..., table_attribute_number: _Optional[int] = ..., name: _Optional[str] = ..., alias: _Optional[str] = ..., table_path: _Optional[str] = ..., data_label: _Optional[str] = ..., data_type: _Optional[str] = ..., data_type_oid: _Optional[int] = ..., data_label_locked_for_sidecar: bool = ..., tags: _Optional[_Iterable[str]] = ..., encrypted: bool = ..., data_labels: _Optional[_Iterable[str]] = ...) -> None: ...
