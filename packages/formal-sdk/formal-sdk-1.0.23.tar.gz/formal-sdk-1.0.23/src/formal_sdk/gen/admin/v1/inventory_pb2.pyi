from .types.v1 import domain_pb2 as _domain_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from ...validate.v1 import validate_pb2 as _validate_pb2
from .types.v1 import list_metadata_pb2 as _list_metadata_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetInventoryFlatOldRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ColumnOld(_message.Message):
    __slots__ = ["created_at", "updated_at", "datastore_id", "datastore_name", "path", "table_physical_id", "table_attribute_number", "name", "alias", "table_path", "data_label", "data_type", "data_type_oid", "data_label_locked_for_sidecar", "tags", "encrypted"]
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
    def __init__(self, created_at: _Optional[int] = ..., updated_at: _Optional[int] = ..., datastore_id: _Optional[str] = ..., datastore_name: _Optional[str] = ..., path: _Optional[str] = ..., table_physical_id: _Optional[str] = ..., table_attribute_number: _Optional[int] = ..., name: _Optional[str] = ..., alias: _Optional[str] = ..., table_path: _Optional[str] = ..., data_label: _Optional[str] = ..., data_type: _Optional[str] = ..., data_type_oid: _Optional[int] = ..., data_label_locked_for_sidecar: bool = ..., tags: _Optional[_Iterable[str]] = ..., encrypted: bool = ...) -> None: ...

class GetInventoryFlatOldResponse(_message.Message):
    __slots__ = ["inventory"]
    INVENTORY_FIELD_NUMBER: _ClassVar[int]
    inventory: _containers.RepeatedCompositeFieldContainer[ColumnOld]
    def __init__(self, inventory: _Optional[_Iterable[_Union[ColumnOld, _Mapping]]] = ...) -> None: ...

class UpdateColumnFieldEncryptionRequest(_message.Message):
    __slots__ = ["datastore_id", "path", "encryption_key_storage", "encryption_key_id", "encryption_algorithm", "encrypt_existing_data"]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTION_KEY_STORAGE_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTION_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTION_ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    ENCRYPT_EXISTING_DATA_FIELD_NUMBER: _ClassVar[int]
    datastore_id: str
    path: str
    encryption_key_storage: str
    encryption_key_id: str
    encryption_algorithm: str
    encrypt_existing_data: bool
    def __init__(self, datastore_id: _Optional[str] = ..., path: _Optional[str] = ..., encryption_key_storage: _Optional[str] = ..., encryption_key_id: _Optional[str] = ..., encryption_algorithm: _Optional[str] = ..., encrypt_existing_data: bool = ...) -> None: ...

class UpdateColumnFieldEncryptionResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetInventoryObjectRequest(_message.Message):
    __slots__ = ["datastore_id", "path"]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    datastore_id: str
    path: str
    def __init__(self, datastore_id: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class GetInventoryObjectResponse(_message.Message):
    __slots__ = ["column"]
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    column: Column
    def __init__(self, column: _Optional[_Union[Column, _Mapping]] = ...) -> None: ...

class GetInventoryHierarchicalRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetInventoryHierarchicalResponse(_message.Message):
    __slots__ = ["inventory"]
    class Datastore(_message.Message):
        __slots__ = ["id", "name", "technology", "dbs"]
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        TECHNOLOGY_FIELD_NUMBER: _ClassVar[int]
        DBS_FIELD_NUMBER: _ClassVar[int]
        id: str
        name: str
        technology: str
        dbs: _containers.RepeatedCompositeFieldContainer[GetInventoryHierarchicalResponse.Db]
        def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., technology: _Optional[str] = ..., dbs: _Optional[_Iterable[_Union[GetInventoryHierarchicalResponse.Db, _Mapping]]] = ...) -> None: ...
    class Db(_message.Message):
        __slots__ = ["path", "name", "datastore_id", "schemas", "tables"]
        PATH_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
        SCHEMAS_FIELD_NUMBER: _ClassVar[int]
        TABLES_FIELD_NUMBER: _ClassVar[int]
        path: str
        name: str
        datastore_id: str
        schemas: _containers.RepeatedCompositeFieldContainer[GetInventoryHierarchicalResponse.Schema]
        tables: _containers.RepeatedCompositeFieldContainer[GetInventoryHierarchicalResponse.Table]
        def __init__(self, path: _Optional[str] = ..., name: _Optional[str] = ..., datastore_id: _Optional[str] = ..., schemas: _Optional[_Iterable[_Union[GetInventoryHierarchicalResponse.Schema, _Mapping]]] = ..., tables: _Optional[_Iterable[_Union[GetInventoryHierarchicalResponse.Table, _Mapping]]] = ...) -> None: ...
    class Schema(_message.Message):
        __slots__ = ["path", "name", "db_path", "tables"]
        PATH_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        DB_PATH_FIELD_NUMBER: _ClassVar[int]
        TABLES_FIELD_NUMBER: _ClassVar[int]
        path: str
        name: str
        db_path: str
        tables: _containers.RepeatedCompositeFieldContainer[GetInventoryHierarchicalResponse.Table]
        def __init__(self, path: _Optional[str] = ..., name: _Optional[str] = ..., db_path: _Optional[str] = ..., tables: _Optional[_Iterable[_Union[GetInventoryHierarchicalResponse.Table, _Mapping]]] = ...) -> None: ...
    class Table(_message.Message):
        __slots__ = ["path", "name", "db_path", "schema_path", "columns"]
        PATH_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        DB_PATH_FIELD_NUMBER: _ClassVar[int]
        SCHEMA_PATH_FIELD_NUMBER: _ClassVar[int]
        COLUMNS_FIELD_NUMBER: _ClassVar[int]
        path: str
        name: str
        db_path: str
        schema_path: str
        columns: _containers.RepeatedCompositeFieldContainer[GetInventoryHierarchicalResponse.Column]
        def __init__(self, path: _Optional[str] = ..., name: _Optional[str] = ..., db_path: _Optional[str] = ..., schema_path: _Optional[str] = ..., columns: _Optional[_Iterable[_Union[GetInventoryHierarchicalResponse.Column, _Mapping]]] = ...) -> None: ...
    class Column(_message.Message):
        __slots__ = ["path", "name", "table_path"]
        PATH_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        TABLE_PATH_FIELD_NUMBER: _ClassVar[int]
        path: str
        name: str
        table_path: str
        def __init__(self, path: _Optional[str] = ..., name: _Optional[str] = ..., table_path: _Optional[str] = ...) -> None: ...
    INVENTORY_FIELD_NUMBER: _ClassVar[int]
    inventory: _containers.RepeatedCompositeFieldContainer[GetInventoryHierarchicalResponse.Datastore]
    def __init__(self, inventory: _Optional[_Iterable[_Union[GetInventoryHierarchicalResponse.Datastore, _Mapping]]] = ...) -> None: ...

class GetInventoryRequest(_message.Message):
    __slots__ = ["limit", "cursor", "order", "path", "excluded_paths", "included_objects"]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_PATHS_FIELD_NUMBER: _ClassVar[int]
    INCLUDED_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    order: str
    path: str
    excluded_paths: _containers.RepeatedScalarFieldContainer[str]
    included_objects: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, limit: _Optional[int] = ..., cursor: _Optional[str] = ..., order: _Optional[str] = ..., path: _Optional[str] = ..., excluded_paths: _Optional[_Iterable[str]] = ..., included_objects: _Optional[_Iterable[str]] = ...) -> None: ...

class GetInventoryResponse(_message.Message):
    __slots__ = ["inventory", "list_metadata"]
    INVENTORY_FIELD_NUMBER: _ClassVar[int]
    LIST_METADATA_FIELD_NUMBER: _ClassVar[int]
    inventory: _containers.RepeatedCompositeFieldContainer[InventoryObject]
    list_metadata: _list_metadata_pb2.ListMetadata
    def __init__(self, inventory: _Optional[_Iterable[_Union[InventoryObject, _Mapping]]] = ..., list_metadata: _Optional[_Union[_list_metadata_pb2.ListMetadata, _Mapping]] = ...) -> None: ...

class GetInventoryFlatRequest(_message.Message):
    __slots__ = ["limit", "after", "before", "order"]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    limit: int
    after: str
    before: str
    order: str
    def __init__(self, limit: _Optional[int] = ..., after: _Optional[str] = ..., before: _Optional[str] = ..., order: _Optional[str] = ...) -> None: ...

class Column(_message.Message):
    __slots__ = ["created_at", "updated_at", "datastore_id", "datastore_name", "path", "table_physical_id", "table_attribute_number", "name", "alias", "table_path", "data_label", "data_type", "data_type_oid", "data_label_locked_for_sidecar", "tags", "encrypted", "id"]
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
    ID_FIELD_NUMBER: _ClassVar[int]
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
    id: str
    def __init__(self, created_at: _Optional[int] = ..., updated_at: _Optional[int] = ..., datastore_id: _Optional[str] = ..., datastore_name: _Optional[str] = ..., path: _Optional[str] = ..., table_physical_id: _Optional[str] = ..., table_attribute_number: _Optional[int] = ..., name: _Optional[str] = ..., alias: _Optional[str] = ..., table_path: _Optional[str] = ..., data_label: _Optional[str] = ..., data_type: _Optional[str] = ..., data_type_oid: _Optional[int] = ..., data_label_locked_for_sidecar: bool = ..., tags: _Optional[_Iterable[str]] = ..., encrypted: bool = ..., id: _Optional[str] = ...) -> None: ...

class Ds(_message.Message):
    __slots__ = ["id", "name", "technology", "dbs"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TECHNOLOGY_FIELD_NUMBER: _ClassVar[int]
    DBS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    technology: str
    dbs: _containers.RepeatedCompositeFieldContainer[Db]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., technology: _Optional[str] = ..., dbs: _Optional[_Iterable[_Union[Db, _Mapping]]] = ...) -> None: ...

class Db(_message.Message):
    __slots__ = ["path", "name", "datastore_id", "schemas", "tables", "id"]
    PATH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    SCHEMAS_FIELD_NUMBER: _ClassVar[int]
    TABLES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    path: str
    name: str
    datastore_id: str
    schemas: _containers.RepeatedCompositeFieldContainer[Schema]
    tables: _containers.RepeatedCompositeFieldContainer[Table]
    id: str
    def __init__(self, path: _Optional[str] = ..., name: _Optional[str] = ..., datastore_id: _Optional[str] = ..., schemas: _Optional[_Iterable[_Union[Schema, _Mapping]]] = ..., tables: _Optional[_Iterable[_Union[Table, _Mapping]]] = ..., id: _Optional[str] = ...) -> None: ...

class Schema(_message.Message):
    __slots__ = ["path", "name", "db_path", "tables", "id", "datastore_id"]
    PATH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DB_PATH_FIELD_NUMBER: _ClassVar[int]
    TABLES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    path: str
    name: str
    db_path: str
    tables: _containers.RepeatedCompositeFieldContainer[Table]
    id: str
    datastore_id: str
    def __init__(self, path: _Optional[str] = ..., name: _Optional[str] = ..., db_path: _Optional[str] = ..., tables: _Optional[_Iterable[_Union[Table, _Mapping]]] = ..., id: _Optional[str] = ..., datastore_id: _Optional[str] = ...) -> None: ...

class Table(_message.Message):
    __slots__ = ["path", "name", "db_path", "schema_path", "columns", "id", "datastore_id"]
    PATH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DB_PATH_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_PATH_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    path: str
    name: str
    db_path: str
    schema_path: str
    columns: _containers.RepeatedCompositeFieldContainer[Column]
    id: str
    datastore_id: str
    def __init__(self, path: _Optional[str] = ..., name: _Optional[str] = ..., db_path: _Optional[str] = ..., schema_path: _Optional[str] = ..., columns: _Optional[_Iterable[_Union[Column, _Mapping]]] = ..., id: _Optional[str] = ..., datastore_id: _Optional[str] = ...) -> None: ...

class SubColumn(_message.Message):
    __slots__ = ["created_at", "updated_at", "datastore_id", "datastore_name", "path", "name", "table_path", "data_label", "data_type", "data_type_oid", "data_label_locked_for_sidecar", "tags", "encrypted", "id"]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_PATH_FIELD_NUMBER: _ClassVar[int]
    DATA_LABEL_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_OID_FIELD_NUMBER: _ClassVar[int]
    DATA_LABEL_LOCKED_FOR_SIDECAR_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    created_at: int
    updated_at: int
    datastore_id: str
    datastore_name: str
    path: str
    name: str
    table_path: str
    data_label: str
    data_type: str
    data_type_oid: int
    data_label_locked_for_sidecar: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    encrypted: bool
    id: str
    def __init__(self, created_at: _Optional[int] = ..., updated_at: _Optional[int] = ..., datastore_id: _Optional[str] = ..., datastore_name: _Optional[str] = ..., path: _Optional[str] = ..., name: _Optional[str] = ..., table_path: _Optional[str] = ..., data_label: _Optional[str] = ..., data_type: _Optional[str] = ..., data_type_oid: _Optional[int] = ..., data_label_locked_for_sidecar: bool = ..., tags: _Optional[_Iterable[str]] = ..., encrypted: bool = ..., id: _Optional[str] = ...) -> None: ...

class InventoryObject(_message.Message):
    __slots__ = ["datastore", "db", "schema", "table", "column", "sub_column"]
    DATASTORE_FIELD_NUMBER: _ClassVar[int]
    DB_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    SUB_COLUMN_FIELD_NUMBER: _ClassVar[int]
    datastore: Ds
    db: Db
    schema: Schema
    table: Table
    column: Column
    sub_column: SubColumn
    def __init__(self, datastore: _Optional[_Union[Ds, _Mapping]] = ..., db: _Optional[_Union[Db, _Mapping]] = ..., schema: _Optional[_Union[Schema, _Mapping]] = ..., table: _Optional[_Union[Table, _Mapping]] = ..., column: _Optional[_Union[Column, _Mapping]] = ..., sub_column: _Optional[_Union[SubColumn, _Mapping]] = ...) -> None: ...

class GetInventoryFlatResponse(_message.Message):
    __slots__ = ["inventory", "list_metadata"]
    INVENTORY_FIELD_NUMBER: _ClassVar[int]
    LIST_METADATA_FIELD_NUMBER: _ClassVar[int]
    inventory: _containers.RepeatedCompositeFieldContainer[InventoryObject]
    list_metadata: _list_metadata_pb2.ListMetadata
    def __init__(self, inventory: _Optional[_Iterable[_Union[InventoryObject, _Mapping]]] = ..., list_metadata: _Optional[_Union[_list_metadata_pb2.ListMetadata, _Mapping]] = ...) -> None: ...

class UpdateColumnLockStatusRequest(_message.Message):
    __slots__ = ["datastore_id", "path", "validated"]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    VALIDATED_FIELD_NUMBER: _ClassVar[int]
    datastore_id: str
    path: str
    validated: bool
    def __init__(self, datastore_id: _Optional[str] = ..., path: _Optional[str] = ..., validated: bool = ...) -> None: ...

class UpdateColumnLockStatusResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UpdateColumnDataLabelRequest(_message.Message):
    __slots__ = ["datastore_id", "path", "data_label"]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    DATA_LABEL_FIELD_NUMBER: _ClassVar[int]
    datastore_id: str
    path: str
    data_label: str
    def __init__(self, datastore_id: _Optional[str] = ..., path: _Optional[str] = ..., data_label: _Optional[str] = ...) -> None: ...

class UpdateColumnDataLabelResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CreateInventoryObjectRequest(_message.Message):
    __slots__ = ["datastore_id", "object_type", "db", "schema", "table", "column", "sub_column"]
    class Db(_message.Message):
        __slots__ = ["path", "name"]
        PATH_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        path: str
        name: str
        def __init__(self, path: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...
    class Schema(_message.Message):
        __slots__ = ["path", "name"]
        PATH_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        path: str
        name: str
        def __init__(self, path: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...
    class Table(_message.Message):
        __slots__ = ["path", "name"]
        PATH_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        path: str
        name: str
        def __init__(self, path: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...
    class Column(_message.Message):
        __slots__ = ["path", "name", "data_type"]
        PATH_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
        path: str
        name: str
        data_type: str
        def __init__(self, path: _Optional[str] = ..., name: _Optional[str] = ..., data_type: _Optional[str] = ...) -> None: ...
    class SubColumn(_message.Message):
        __slots__ = ["path", "name", "sub_type"]
        PATH_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        SUB_TYPE_FIELD_NUMBER: _ClassVar[int]
        path: str
        name: str
        sub_type: str
        def __init__(self, path: _Optional[str] = ..., name: _Optional[str] = ..., sub_type: _Optional[str] = ...) -> None: ...
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    DB_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    SUB_COLUMN_FIELD_NUMBER: _ClassVar[int]
    datastore_id: str
    object_type: str
    db: CreateInventoryObjectRequest.Db
    schema: CreateInventoryObjectRequest.Schema
    table: CreateInventoryObjectRequest.Table
    column: CreateInventoryObjectRequest.Column
    sub_column: CreateInventoryObjectRequest.SubColumn
    def __init__(self, datastore_id: _Optional[str] = ..., object_type: _Optional[str] = ..., db: _Optional[_Union[CreateInventoryObjectRequest.Db, _Mapping]] = ..., schema: _Optional[_Union[CreateInventoryObjectRequest.Schema, _Mapping]] = ..., table: _Optional[_Union[CreateInventoryObjectRequest.Table, _Mapping]] = ..., column: _Optional[_Union[CreateInventoryObjectRequest.Column, _Mapping]] = ..., sub_column: _Optional[_Union[CreateInventoryObjectRequest.SubColumn, _Mapping]] = ...) -> None: ...

class CreateInventoryObjectResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteInventoryObjectRequest(_message.Message):
    __slots__ = ["datastore_id", "path"]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    datastore_id: str
    path: str
    def __init__(self, datastore_id: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class DeleteInventoryObjectResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Tag(_message.Message):
    __slots__ = ["id", "name", "created_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreateInventoryTagRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class CreateInventoryTagResponse(_message.Message):
    __slots__ = ["tag"]
    TAG_FIELD_NUMBER: _ClassVar[int]
    tag: Tag
    def __init__(self, tag: _Optional[_Union[Tag, _Mapping]] = ...) -> None: ...

class GetInventoryTagsRequest(_message.Message):
    __slots__ = ["limit", "after", "before", "order"]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    limit: int
    after: str
    before: str
    order: str
    def __init__(self, limit: _Optional[int] = ..., after: _Optional[str] = ..., before: _Optional[str] = ..., order: _Optional[str] = ...) -> None: ...

class GetInventoryTagsResponse(_message.Message):
    __slots__ = ["tags", "list_metadata"]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    LIST_METADATA_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.RepeatedCompositeFieldContainer[Tag]
    list_metadata: _list_metadata_pb2.ListMetadata
    def __init__(self, tags: _Optional[_Iterable[_Union[Tag, _Mapping]]] = ..., list_metadata: _Optional[_Union[_list_metadata_pb2.ListMetadata, _Mapping]] = ...) -> None: ...

class UpdateInventoryObjectTagsRequest(_message.Message):
    __slots__ = ["datastore_id", "path", "tags"]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    datastore_id: str
    path: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, datastore_id: _Optional[str] = ..., path: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateInventoryObjectTagsResponse(_message.Message):
    __slots__ = ["object"]
    class InventoryObject(_message.Message):
        __slots__ = ["datastore_id", "type", "path", "db_path", "table_path", "schema_path", "table_attribute_number", "data_type", "data_label", "updated_at", "created_at", "data_store_name", "name", "validated", "tags"]
        DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        PATH_FIELD_NUMBER: _ClassVar[int]
        DB_PATH_FIELD_NUMBER: _ClassVar[int]
        TABLE_PATH_FIELD_NUMBER: _ClassVar[int]
        SCHEMA_PATH_FIELD_NUMBER: _ClassVar[int]
        TABLE_ATTRIBUTE_NUMBER_FIELD_NUMBER: _ClassVar[int]
        DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
        DATA_LABEL_FIELD_NUMBER: _ClassVar[int]
        UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
        CREATED_AT_FIELD_NUMBER: _ClassVar[int]
        DATA_STORE_NAME_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALIDATED_FIELD_NUMBER: _ClassVar[int]
        TAGS_FIELD_NUMBER: _ClassVar[int]
        datastore_id: str
        type: str
        path: str
        db_path: str
        table_path: str
        schema_path: str
        table_attribute_number: int
        data_type: str
        data_label: str
        updated_at: int
        created_at: int
        data_store_name: str
        name: str
        validated: bool
        tags: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, datastore_id: _Optional[str] = ..., type: _Optional[str] = ..., path: _Optional[str] = ..., db_path: _Optional[str] = ..., table_path: _Optional[str] = ..., schema_path: _Optional[str] = ..., table_attribute_number: _Optional[int] = ..., data_type: _Optional[str] = ..., data_label: _Optional[str] = ..., updated_at: _Optional[int] = ..., created_at: _Optional[int] = ..., data_store_name: _Optional[str] = ..., name: _Optional[str] = ..., validated: bool = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    object: UpdateInventoryObjectTagsResponse.InventoryObject
    def __init__(self, object: _Optional[_Union[UpdateInventoryObjectTagsResponse.InventoryObject, _Mapping]] = ...) -> None: ...

class DeleteInventoryTagRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteInventoryTagResponse(_message.Message):
    __slots__ = ["tags"]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.RepeatedCompositeFieldContainer[Tag]
    def __init__(self, tags: _Optional[_Iterable[_Union[Tag, _Mapping]]] = ...) -> None: ...

class GetInventoryMetricsRequest(_message.Message):
    __slots__ = ["user_id", "datastore_id", "path", "object_type", "timeframe"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIMEFRAME_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    datastore_id: str
    path: str
    object_type: str
    timeframe: str
    def __init__(self, user_id: _Optional[str] = ..., datastore_id: _Optional[str] = ..., path: _Optional[str] = ..., object_type: _Optional[str] = ..., timeframe: _Optional[str] = ...) -> None: ...

class GetInventoryMetricsResponse(_message.Message):
    __slots__ = ["metrics"]
    class Metric(_message.Message):
        __slots__ = ["name", "path", "column_name", "column_path", "table_name", "table_path", "schema_name", "schema_path", "db_name", "user_id", "db_user", "end_user_id", "end_user_db_username", "app_type", "org_id", "datastore_id", "datastore_name", "ts", "counter", "returned_rows", "ip_address", "data_label", "data_labels", "datastore_technology", "bucket"]
        NAME_FIELD_NUMBER: _ClassVar[int]
        PATH_FIELD_NUMBER: _ClassVar[int]
        COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
        COLUMN_PATH_FIELD_NUMBER: _ClassVar[int]
        TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
        TABLE_PATH_FIELD_NUMBER: _ClassVar[int]
        SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
        SCHEMA_PATH_FIELD_NUMBER: _ClassVar[int]
        DB_NAME_FIELD_NUMBER: _ClassVar[int]
        USER_ID_FIELD_NUMBER: _ClassVar[int]
        DB_USER_FIELD_NUMBER: _ClassVar[int]
        END_USER_ID_FIELD_NUMBER: _ClassVar[int]
        END_USER_DB_USERNAME_FIELD_NUMBER: _ClassVar[int]
        APP_TYPE_FIELD_NUMBER: _ClassVar[int]
        ORG_ID_FIELD_NUMBER: _ClassVar[int]
        DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
        DATASTORE_NAME_FIELD_NUMBER: _ClassVar[int]
        TS_FIELD_NUMBER: _ClassVar[int]
        COUNTER_FIELD_NUMBER: _ClassVar[int]
        RETURNED_ROWS_FIELD_NUMBER: _ClassVar[int]
        IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
        DATA_LABEL_FIELD_NUMBER: _ClassVar[int]
        DATA_LABELS_FIELD_NUMBER: _ClassVar[int]
        DATASTORE_TECHNOLOGY_FIELD_NUMBER: _ClassVar[int]
        BUCKET_FIELD_NUMBER: _ClassVar[int]
        name: str
        path: str
        column_name: str
        column_path: str
        table_name: str
        table_path: str
        schema_name: str
        schema_path: str
        db_name: str
        user_id: str
        db_user: str
        end_user_id: str
        end_user_db_username: str
        app_type: str
        org_id: str
        datastore_id: str
        datastore_name: str
        ts: str
        counter: int
        returned_rows: int
        ip_address: str
        data_label: str
        data_labels: _containers.RepeatedScalarFieldContainer[str]
        datastore_technology: str
        bucket: str
        def __init__(self, name: _Optional[str] = ..., path: _Optional[str] = ..., column_name: _Optional[str] = ..., column_path: _Optional[str] = ..., table_name: _Optional[str] = ..., table_path: _Optional[str] = ..., schema_name: _Optional[str] = ..., schema_path: _Optional[str] = ..., db_name: _Optional[str] = ..., user_id: _Optional[str] = ..., db_user: _Optional[str] = ..., end_user_id: _Optional[str] = ..., end_user_db_username: _Optional[str] = ..., app_type: _Optional[str] = ..., org_id: _Optional[str] = ..., datastore_id: _Optional[str] = ..., datastore_name: _Optional[str] = ..., ts: _Optional[str] = ..., counter: _Optional[int] = ..., returned_rows: _Optional[int] = ..., ip_address: _Optional[str] = ..., data_label: _Optional[str] = ..., data_labels: _Optional[_Iterable[str]] = ..., datastore_technology: _Optional[str] = ..., bucket: _Optional[str] = ...) -> None: ...
    METRICS_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[GetInventoryMetricsResponse.Metric]
    def __init__(self, metrics: _Optional[_Iterable[_Union[GetInventoryMetricsResponse.Metric, _Mapping]]] = ...) -> None: ...

class CreateDataDomainRequest(_message.Message):
    __slots__ = ["name", "description", "owners", "excluded_paths", "included_paths"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OWNERS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_PATHS_FIELD_NUMBER: _ClassVar[int]
    INCLUDED_PATHS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    owners: _containers.RepeatedCompositeFieldContainer[_domain_pb2.Owner]
    excluded_paths: _containers.RepeatedScalarFieldContainer[str]
    included_paths: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., owners: _Optional[_Iterable[_Union[_domain_pb2.Owner, _Mapping]]] = ..., excluded_paths: _Optional[_Iterable[str]] = ..., included_paths: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateDataDomainResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetDataDomainsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetDataDomainsResponse(_message.Message):
    __slots__ = ["domains"]
    DOMAINS_FIELD_NUMBER: _ClassVar[int]
    domains: _containers.RepeatedCompositeFieldContainer[_domain_pb2.Domain]
    def __init__(self, domains: _Optional[_Iterable[_Union[_domain_pb2.Domain, _Mapping]]] = ...) -> None: ...

class GetDataDomainByIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetDataDomainByIdResponse(_message.Message):
    __slots__ = ["domain"]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    domain: _domain_pb2.Domain
    def __init__(self, domain: _Optional[_Union[_domain_pb2.Domain, _Mapping]] = ...) -> None: ...

class UpdateDataDomainRequest(_message.Message):
    __slots__ = ["id", "name", "description", "owners", "excluded_paths", "included_paths"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OWNERS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_PATHS_FIELD_NUMBER: _ClassVar[int]
    INCLUDED_PATHS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    owners: _containers.RepeatedCompositeFieldContainer[_domain_pb2.Owner]
    excluded_paths: _containers.RepeatedScalarFieldContainer[str]
    included_paths: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., owners: _Optional[_Iterable[_Union[_domain_pb2.Owner, _Mapping]]] = ..., excluded_paths: _Optional[_Iterable[str]] = ..., included_paths: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateDataDomainResponse(_message.Message):
    __slots__ = ["domain"]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    domain: _domain_pb2.Domain
    def __init__(self, domain: _Optional[_Union[_domain_pb2.Domain, _Mapping]] = ...) -> None: ...

class DeleteDataDomainRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteDataDomainResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
