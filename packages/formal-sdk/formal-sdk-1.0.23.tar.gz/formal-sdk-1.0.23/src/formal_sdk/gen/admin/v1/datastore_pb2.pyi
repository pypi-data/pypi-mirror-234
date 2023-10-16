from .types.v1 import list_metadata_pb2 as _list_metadata_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateDatastoreRequest(_message.Message):
    __slots__ = ["name", "hostname", "port", "technology", "health_check_db_name", "db_discovery_job_wait_time", "db_discovery_native_role_id", "environment"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    TECHNOLOGY_FIELD_NUMBER: _ClassVar[int]
    HEALTH_CHECK_DB_NAME_FIELD_NUMBER: _ClassVar[int]
    DB_DISCOVERY_JOB_WAIT_TIME_FIELD_NUMBER: _ClassVar[int]
    DB_DISCOVERY_NATIVE_ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    name: str
    hostname: str
    port: int
    technology: str
    health_check_db_name: str
    db_discovery_job_wait_time: str
    db_discovery_native_role_id: str
    environment: str
    def __init__(self, name: _Optional[str] = ..., hostname: _Optional[str] = ..., port: _Optional[int] = ..., technology: _Optional[str] = ..., health_check_db_name: _Optional[str] = ..., db_discovery_job_wait_time: _Optional[str] = ..., db_discovery_native_role_id: _Optional[str] = ..., environment: _Optional[str] = ...) -> None: ...

class CreateDatastoreResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetDatastoreRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetDatastoreResponse(_message.Message):
    __slots__ = ["datastore"]
    DATASTORE_FIELD_NUMBER: _ClassVar[int]
    datastore: Datastore
    def __init__(self, datastore: _Optional[_Union[Datastore, _Mapping]] = ...) -> None: ...

class GetDatastoresRequest(_message.Message):
    __slots__ = ["limit", "cursor", "order", "filter"]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    order: str
    filter: str
    def __init__(self, limit: _Optional[int] = ..., cursor: _Optional[str] = ..., order: _Optional[str] = ..., filter: _Optional[str] = ...) -> None: ...

class GetDatastoresResponse(_message.Message):
    __slots__ = ["datastores", "list_metadata"]
    DATASTORES_FIELD_NUMBER: _ClassVar[int]
    LIST_METADATA_FIELD_NUMBER: _ClassVar[int]
    datastores: _containers.RepeatedCompositeFieldContainer[Datastore]
    list_metadata: _list_metadata_pb2.ListMetadata
    def __init__(self, datastores: _Optional[_Iterable[_Union[Datastore, _Mapping]]] = ..., list_metadata: _Optional[_Union[_list_metadata_pb2.ListMetadata, _Mapping]] = ...) -> None: ...

class DeleteDatastoreRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteDatastoreResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UpdateDatastoreNameRequest(_message.Message):
    __slots__ = ["id", "name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class UpdateDatastoreNameResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UpdateDbDiscoveryConfigRequest(_message.Message):
    __slots__ = ["id", "db_discovery_job_wait_time", "db_discovery_native_role_id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    DB_DISCOVERY_JOB_WAIT_TIME_FIELD_NUMBER: _ClassVar[int]
    DB_DISCOVERY_NATIVE_ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    db_discovery_job_wait_time: str
    db_discovery_native_role_id: str
    def __init__(self, id: _Optional[str] = ..., db_discovery_job_wait_time: _Optional[str] = ..., db_discovery_native_role_id: _Optional[str] = ...) -> None: ...

class UpdateDbDiscoveryConfigResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UpdateDataStoreHealthCheckDbNameRequest(_message.Message):
    __slots__ = ["id", "health_check_db_name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    HEALTH_CHECK_DB_NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    health_check_db_name: str
    def __init__(self, id: _Optional[str] = ..., health_check_db_name: _Optional[str] = ...) -> None: ...

class UpdateDataStoreHealthCheckDbNameResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UpdateDataStoreDefaultAccessBehaviorRequest(_message.Message):
    __slots__ = ["id", "default_access_behavior"]
    ID_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ACCESS_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    default_access_behavior: str
    def __init__(self, id: _Optional[str] = ..., default_access_behavior: _Optional[str] = ...) -> None: ...

class UpdateDataStoreDefaultAccessBehaviorResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetLinkedSidecarsRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetLinkedSidecarsResponse(_message.Message):
    __slots__ = ["sidecars"]
    SIDECARS_FIELD_NUMBER: _ClassVar[int]
    sidecars: _containers.RepeatedCompositeFieldContainer[LinkedSidecar]
    def __init__(self, sidecars: _Optional[_Iterable[_Union[LinkedSidecar, _Mapping]]] = ...) -> None: ...

class LinkedSidecar(_message.Message):
    __slots__ = ["id", "name", "hostname"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    hostname: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., hostname: _Optional[str] = ...) -> None: ...

class Datastore(_message.Message):
    __slots__ = ["id", "datastore_id", "name", "port", "hostname", "health_check_db_name", "technology", "created_at", "expire_at", "db_discovery_job_wait_time", "db_discovery_native_role_id", "default_access_behavior", "linked_logs", "environment"]
    ID_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    HEALTH_CHECK_DB_NAME_FIELD_NUMBER: _ClassVar[int]
    TECHNOLOGY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_AT_FIELD_NUMBER: _ClassVar[int]
    DB_DISCOVERY_JOB_WAIT_TIME_FIELD_NUMBER: _ClassVar[int]
    DB_DISCOVERY_NATIVE_ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ACCESS_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    LINKED_LOGS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    id: str
    datastore_id: str
    name: str
    port: int
    hostname: str
    health_check_db_name: str
    technology: str
    created_at: _timestamp_pb2.Timestamp
    expire_at: str
    db_discovery_job_wait_time: str
    db_discovery_native_role_id: str
    default_access_behavior: str
    linked_logs: _containers.RepeatedCompositeFieldContainer[IntegrationLog]
    environment: str
    def __init__(self, id: _Optional[str] = ..., datastore_id: _Optional[str] = ..., name: _Optional[str] = ..., port: _Optional[int] = ..., hostname: _Optional[str] = ..., health_check_db_name: _Optional[str] = ..., technology: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., expire_at: _Optional[str] = ..., db_discovery_job_wait_time: _Optional[str] = ..., db_discovery_native_role_id: _Optional[str] = ..., default_access_behavior: _Optional[str] = ..., linked_logs: _Optional[_Iterable[_Union[IntegrationLog, _Mapping]]] = ..., environment: _Optional[str] = ...) -> None: ...

class IntegrationLog(_message.Message):
    __slots__ = ["id", "name", "type", "created_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    type: str
    created_at: int
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[str] = ..., created_at: _Optional[int] = ...) -> None: ...
