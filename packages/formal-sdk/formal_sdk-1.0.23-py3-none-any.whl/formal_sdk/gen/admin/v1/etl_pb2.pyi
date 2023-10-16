from .types.v1 import etl_pb2 as _etl_pb2
from .types.v1 import datastore_pb2 as _datastore_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetGroupsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetGroupsResponse(_message.Message):
    __slots__ = ["groups"]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    groups: _containers.RepeatedCompositeFieldContainer[_etl_pb2.ETLGroup]
    def __init__(self, groups: _Optional[_Iterable[_Union[_etl_pb2.ETLGroup, _Mapping]]] = ...) -> None: ...

class GetConnectorsRequest(_message.Message):
    __slots__ = ["hostname"]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    hostname: str
    def __init__(self, hostname: _Optional[str] = ...) -> None: ...

class GetConnectorsResponse(_message.Message):
    __slots__ = ["connectors"]
    CONNECTORS_FIELD_NUMBER: _ClassVar[int]
    connectors: _containers.RepeatedCompositeFieldContainer[_etl_pb2.ETLConnector]
    def __init__(self, connectors: _Optional[_Iterable[_Union[_etl_pb2.ETLConnector, _Mapping]]] = ...) -> None: ...

class GetConnectorByDbNameRequest(_message.Message):
    __slots__ = ["hostname", "db_name"]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    DB_NAME_FIELD_NUMBER: _ClassVar[int]
    hostname: str
    db_name: str
    def __init__(self, hostname: _Optional[str] = ..., db_name: _Optional[str] = ...) -> None: ...

class GetConnectorByDbNameResponse(_message.Message):
    __slots__ = ["connector", "datastore"]
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_FIELD_NUMBER: _ClassVar[int]
    connector: _etl_pb2.ETLConnector
    datastore: _datastore_pb2.Datastore
    def __init__(self, connector: _Optional[_Union[_etl_pb2.ETLConnector, _Mapping]] = ..., datastore: _Optional[_Union[_datastore_pb2.Datastore, _Mapping]] = ...) -> None: ...

class GetDestinationsRequest(_message.Message):
    __slots__ = ["hostname"]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    hostname: str
    def __init__(self, hostname: _Optional[str] = ...) -> None: ...

class GetDestinationsResponse(_message.Message):
    __slots__ = ["destinations"]
    DESTINATIONS_FIELD_NUMBER: _ClassVar[int]
    destinations: _containers.RepeatedCompositeFieldContainer[_etl_pb2.ETLDestination]
    def __init__(self, destinations: _Optional[_Iterable[_Union[_etl_pb2.ETLDestination, _Mapping]]] = ...) -> None: ...

class GetDestinationByIDRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetDestinationByIDResponse(_message.Message):
    __slots__ = ["destination", "datastore"]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_FIELD_NUMBER: _ClassVar[int]
    destination: _etl_pb2.ETLDestination
    datastore: _datastore_pb2.Datastore
    def __init__(self, destination: _Optional[_Union[_etl_pb2.ETLDestination, _Mapping]] = ..., datastore: _Optional[_Union[_datastore_pb2.Datastore, _Mapping]] = ...) -> None: ...

class GetLineageSchemasRequest(_message.Message):
    __slots__ = ["connector_id"]
    CONNECTOR_ID_FIELD_NUMBER: _ClassVar[int]
    connector_id: str
    def __init__(self, connector_id: _Optional[str] = ...) -> None: ...

class GetLineageSchemasResponse(_message.Message):
    __slots__ = ["schemas"]
    SCHEMAS_FIELD_NUMBER: _ClassVar[int]
    schemas: _containers.RepeatedCompositeFieldContainer[_etl_pb2.ETLSchemaLineage]
    def __init__(self, schemas: _Optional[_Iterable[_Union[_etl_pb2.ETLSchemaLineage, _Mapping]]] = ...) -> None: ...

class GetLineageSchemaByNameRequest(_message.Message):
    __slots__ = ["connector_id", "schema_name"]
    CONNECTOR_ID_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    connector_id: str
    schema_name: str
    def __init__(self, connector_id: _Optional[str] = ..., schema_name: _Optional[str] = ...) -> None: ...

class GetLineageSchemaByNameResponse(_message.Message):
    __slots__ = ["schema"]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    schema: _etl_pb2.ETLSchemaLineage
    def __init__(self, schema: _Optional[_Union[_etl_pb2.ETLSchemaLineage, _Mapping]] = ...) -> None: ...

class GetLineageTablesRequest(_message.Message):
    __slots__ = ["connector_id"]
    CONNECTOR_ID_FIELD_NUMBER: _ClassVar[int]
    connector_id: str
    def __init__(self, connector_id: _Optional[str] = ...) -> None: ...

class GetLineageTablesResponse(_message.Message):
    __slots__ = ["tables"]
    TABLES_FIELD_NUMBER: _ClassVar[int]
    tables: _containers.RepeatedCompositeFieldContainer[_etl_pb2.ETLTableLineage]
    def __init__(self, tables: _Optional[_Iterable[_Union[_etl_pb2.ETLTableLineage, _Mapping]]] = ...) -> None: ...

class GetLineageTableByNameRequest(_message.Message):
    __slots__ = ["connector_id", "schema_id", "table_name"]
    CONNECTOR_ID_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_ID_FIELD_NUMBER: _ClassVar[int]
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    connector_id: str
    schema_id: str
    table_name: str
    def __init__(self, connector_id: _Optional[str] = ..., schema_id: _Optional[str] = ..., table_name: _Optional[str] = ...) -> None: ...

class GetLineageTableByNameResponse(_message.Message):
    __slots__ = ["table"]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    table: _etl_pb2.ETLTableLineage
    def __init__(self, table: _Optional[_Union[_etl_pb2.ETLTableLineage, _Mapping]] = ...) -> None: ...

class GetLineageColumnsRequest(_message.Message):
    __slots__ = ["connector_id"]
    CONNECTOR_ID_FIELD_NUMBER: _ClassVar[int]
    connector_id: str
    def __init__(self, connector_id: _Optional[str] = ...) -> None: ...

class GetLineageColumnsResponse(_message.Message):
    __slots__ = ["columns"]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    columns: _containers.RepeatedCompositeFieldContainer[_etl_pb2.ETLColumnLineage]
    def __init__(self, columns: _Optional[_Iterable[_Union[_etl_pb2.ETLColumnLineage, _Mapping]]] = ...) -> None: ...

class GetLineageColumnsByTableRequest(_message.Message):
    __slots__ = ["connector_id", "table_id"]
    CONNECTOR_ID_FIELD_NUMBER: _ClassVar[int]
    TABLE_ID_FIELD_NUMBER: _ClassVar[int]
    connector_id: str
    table_id: str
    def __init__(self, connector_id: _Optional[str] = ..., table_id: _Optional[str] = ...) -> None: ...

class GetLineageColumnsByTableResponse(_message.Message):
    __slots__ = ["columns"]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    columns: _containers.RepeatedCompositeFieldContainer[_etl_pb2.ETLColumnLineage]
    def __init__(self, columns: _Optional[_Iterable[_Union[_etl_pb2.ETLColumnLineage, _Mapping]]] = ...) -> None: ...
