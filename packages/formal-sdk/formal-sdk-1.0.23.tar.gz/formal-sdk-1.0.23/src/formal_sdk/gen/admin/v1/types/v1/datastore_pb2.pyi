from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Datastore(_message.Message):
    __slots__ = ["id", "created_at", "datastore_id", "name", "original_hostname", "port", "technology", "health_check_db_name", "default_access_behavior", "db_discovery_job_wait_time", "db_discovery_native_role_id", "username", "password", "environment"]
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    TECHNOLOGY_FIELD_NUMBER: _ClassVar[int]
    HEALTH_CHECK_DB_NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ACCESS_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    DB_DISCOVERY_JOB_WAIT_TIME_FIELD_NUMBER: _ClassVar[int]
    DB_DISCOVERY_NATIVE_ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    id: str
    created_at: int
    datastore_id: str
    name: str
    original_hostname: str
    port: int
    technology: str
    health_check_db_name: str
    default_access_behavior: str
    db_discovery_job_wait_time: str
    db_discovery_native_role_id: str
    username: str
    password: str
    environment: str
    def __init__(self, id: _Optional[str] = ..., created_at: _Optional[int] = ..., datastore_id: _Optional[str] = ..., name: _Optional[str] = ..., original_hostname: _Optional[str] = ..., port: _Optional[int] = ..., technology: _Optional[str] = ..., health_check_db_name: _Optional[str] = ..., default_access_behavior: _Optional[str] = ..., db_discovery_job_wait_time: _Optional[str] = ..., db_discovery_native_role_id: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., environment: _Optional[str] = ...) -> None: ...
