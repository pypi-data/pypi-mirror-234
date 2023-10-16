from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ETLGroup(_message.Message):
    __slots__ = ["id", "org_id", "platform_id", "name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    org_id: str
    platform_id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., org_id: _Optional[str] = ..., platform_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class ETLConnector(_message.Message):
    __slots__ = ["id", "org_id", "platform_id", "destination_id", "group_id", "connector_type", "service_name", "host_name", "database_name", "last_synced"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    HOST_NAME_FIELD_NUMBER: _ClassVar[int]
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_SYNCED_FIELD_NUMBER: _ClassVar[int]
    id: str
    org_id: str
    platform_id: str
    destination_id: str
    group_id: str
    connector_type: str
    service_name: str
    host_name: str
    database_name: str
    last_synced: int
    def __init__(self, id: _Optional[str] = ..., org_id: _Optional[str] = ..., platform_id: _Optional[str] = ..., destination_id: _Optional[str] = ..., group_id: _Optional[str] = ..., connector_type: _Optional[str] = ..., service_name: _Optional[str] = ..., host_name: _Optional[str] = ..., database_name: _Optional[str] = ..., last_synced: _Optional[int] = ...) -> None: ...

class ETLDestination(_message.Message):
    __slots__ = ["id", "org_id", "platform_id", "group_id", "destination_type", "service_name", "host_name", "database_name", "last_synced"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    HOST_NAME_FIELD_NUMBER: _ClassVar[int]
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_SYNCED_FIELD_NUMBER: _ClassVar[int]
    id: str
    org_id: str
    platform_id: str
    group_id: str
    destination_type: str
    service_name: str
    host_name: str
    database_name: str
    last_synced: int
    def __init__(self, id: _Optional[str] = ..., org_id: _Optional[str] = ..., platform_id: _Optional[str] = ..., group_id: _Optional[str] = ..., destination_type: _Optional[str] = ..., service_name: _Optional[str] = ..., host_name: _Optional[str] = ..., database_name: _Optional[str] = ..., last_synced: _Optional[int] = ...) -> None: ...

class ETLSchemaLineage(_message.Message):
    __slots__ = ["id", "org_id", "platform_id", "connector_id", "destination_id", "source_schema", "destination_schema", "last_updated"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    id: str
    org_id: str
    platform_id: str
    connector_id: str
    destination_id: str
    source_schema: str
    destination_schema: str
    last_updated: int
    def __init__(self, id: _Optional[str] = ..., org_id: _Optional[str] = ..., platform_id: _Optional[str] = ..., connector_id: _Optional[str] = ..., destination_id: _Optional[str] = ..., source_schema: _Optional[str] = ..., destination_schema: _Optional[str] = ..., last_updated: _Optional[int] = ...) -> None: ...

class ETLTableLineage(_message.Message):
    __slots__ = ["id", "org_id", "platform_id", "connector_id", "destination_id", "schema_id", "source_table", "destination_table", "last_updated"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ID_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TABLE_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_TABLE_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    id: str
    org_id: str
    platform_id: str
    connector_id: str
    destination_id: str
    schema_id: str
    source_table: str
    destination_table: str
    last_updated: int
    def __init__(self, id: _Optional[str] = ..., org_id: _Optional[str] = ..., platform_id: _Optional[str] = ..., connector_id: _Optional[str] = ..., destination_id: _Optional[str] = ..., schema_id: _Optional[str] = ..., source_table: _Optional[str] = ..., destination_table: _Optional[str] = ..., last_updated: _Optional[int] = ...) -> None: ...

class ETLColumnLineage(_message.Message):
    __slots__ = ["id", "org_id", "platform_id", "connector_id", "destination_id", "schema_id", "table_id", "source_column", "destination_column", "source_data_type", "destination_data_type", "is_primary_key", "is_foreign_key"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ID_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_ID_FIELD_NUMBER: _ClassVar[int]
    TABLE_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_COLUMN_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_COLUMN_FIELD_NUMBER: _ClassVar[int]
    SOURCE_DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_PRIMARY_KEY_FIELD_NUMBER: _ClassVar[int]
    IS_FOREIGN_KEY_FIELD_NUMBER: _ClassVar[int]
    id: str
    org_id: str
    platform_id: str
    connector_id: str
    destination_id: str
    schema_id: str
    table_id: str
    source_column: str
    destination_column: str
    source_data_type: str
    destination_data_type: str
    is_primary_key: bool
    is_foreign_key: bool
    def __init__(self, id: _Optional[str] = ..., org_id: _Optional[str] = ..., platform_id: _Optional[str] = ..., connector_id: _Optional[str] = ..., destination_id: _Optional[str] = ..., schema_id: _Optional[str] = ..., table_id: _Optional[str] = ..., source_column: _Optional[str] = ..., destination_column: _Optional[str] = ..., source_data_type: _Optional[str] = ..., destination_data_type: _Optional[str] = ..., is_primary_key: bool = ..., is_foreign_key: bool = ...) -> None: ...

class ETLMapping(_message.Message):
    __slots__ = ["id", "org_id", "connector_id", "platform_connector_id", "platform_type", "last_synced"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_ID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_CONNECTOR_ID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_TYPE_FIELD_NUMBER: _ClassVar[int]
    LAST_SYNCED_FIELD_NUMBER: _ClassVar[int]
    id: str
    org_id: str
    connector_id: str
    platform_connector_id: str
    platform_type: str
    last_synced: int
    def __init__(self, id: _Optional[str] = ..., org_id: _Optional[str] = ..., connector_id: _Optional[str] = ..., platform_connector_id: _Optional[str] = ..., platform_type: _Optional[str] = ..., last_synced: _Optional[int] = ...) -> None: ...
