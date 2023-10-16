from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetMetricsRequest(_message.Message):
    __slots__ = ["datastore_id", "interval", "user_id"]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    datastore_id: _containers.RepeatedScalarFieldContainer[str]
    interval: str
    user_id: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, datastore_id: _Optional[_Iterable[str]] = ..., interval: _Optional[str] = ..., user_id: _Optional[_Iterable[str]] = ...) -> None: ...

class Metric(_message.Message):
    __slots__ = ["name", "path", "column_name", "column_path", "table_name", "table_path", "schema_name", "schema_path", "db_name", "user_id", "db_user", "end_user_id", "end_user_db_username", "app_type", "datastore_id", "datastore_name", "ts", "counter", "returned_rows", "ip_address", "data_label", "data_labels", "datastore_technology", "bucket"]
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
    datastore_id: str
    datastore_name: str
    ts: _timestamp_pb2.Timestamp
    counter: int
    returned_rows: int
    ip_address: str
    data_label: str
    data_labels: _containers.RepeatedScalarFieldContainer[str]
    datastore_technology: str
    bucket: _timestamp_pb2.Timestamp
    def __init__(self, name: _Optional[str] = ..., path: _Optional[str] = ..., column_name: _Optional[str] = ..., column_path: _Optional[str] = ..., table_name: _Optional[str] = ..., table_path: _Optional[str] = ..., schema_name: _Optional[str] = ..., schema_path: _Optional[str] = ..., db_name: _Optional[str] = ..., user_id: _Optional[str] = ..., db_user: _Optional[str] = ..., end_user_id: _Optional[str] = ..., end_user_db_username: _Optional[str] = ..., app_type: _Optional[str] = ..., datastore_id: _Optional[str] = ..., datastore_name: _Optional[str] = ..., ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., counter: _Optional[int] = ..., returned_rows: _Optional[int] = ..., ip_address: _Optional[str] = ..., data_label: _Optional[str] = ..., data_labels: _Optional[_Iterable[str]] = ..., datastore_technology: _Optional[str] = ..., bucket: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Node(_message.Message):
    __slots__ = ["id", "type", "shape", "color", "label"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    shape: str
    color: str
    label: str
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ..., shape: _Optional[str] = ..., color: _Optional[str] = ..., label: _Optional[str] = ...) -> None: ...

class Link(_message.Message):
    __slots__ = ["source", "target"]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    source: str
    target: str
    def __init__(self, source: _Optional[str] = ..., target: _Optional[str] = ...) -> None: ...

class GetMetricsResponse(_message.Message):
    __slots__ = ["metrics", "nodes", "links"]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[Metric]
    nodes: _containers.RepeatedCompositeFieldContainer[Node]
    links: _containers.RepeatedCompositeFieldContainer[Link]
    def __init__(self, metrics: _Optional[_Iterable[_Union[Metric, _Mapping]]] = ..., nodes: _Optional[_Iterable[_Union[Node, _Mapping]]] = ..., links: _Optional[_Iterable[_Union[Link, _Mapping]]] = ...) -> None: ...

class RowLevelMetric(_message.Message):
    __slots__ = ["datastore_id", "datastore_name", "end_user_id", "end_user_db_username", "user_id", "db_user", "db_name", "schema_name", "table_name", "path", "hashed_row_level_value", "clear_text_row_level_value", "timestamp", "queries_count", "rows_count", "time_bucket"]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_NAME_FIELD_NUMBER: _ClassVar[int]
    END_USER_ID_FIELD_NUMBER: _ClassVar[int]
    END_USER_DB_USERNAME_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    DB_USER_FIELD_NUMBER: _ClassVar[int]
    DB_NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    HASHED_ROW_LEVEL_VALUE_FIELD_NUMBER: _ClassVar[int]
    CLEAR_TEXT_ROW_LEVEL_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    QUERIES_COUNT_FIELD_NUMBER: _ClassVar[int]
    ROWS_COUNT_FIELD_NUMBER: _ClassVar[int]
    TIME_BUCKET_FIELD_NUMBER: _ClassVar[int]
    datastore_id: str
    datastore_name: str
    end_user_id: str
    end_user_db_username: str
    user_id: str
    db_user: str
    db_name: str
    schema_name: str
    table_name: str
    path: str
    hashed_row_level_value: str
    clear_text_row_level_value: str
    timestamp: _timestamp_pb2.Timestamp
    queries_count: int
    rows_count: int
    time_bucket: _timestamp_pb2.Timestamp
    def __init__(self, datastore_id: _Optional[str] = ..., datastore_name: _Optional[str] = ..., end_user_id: _Optional[str] = ..., end_user_db_username: _Optional[str] = ..., user_id: _Optional[str] = ..., db_user: _Optional[str] = ..., db_name: _Optional[str] = ..., schema_name: _Optional[str] = ..., table_name: _Optional[str] = ..., path: _Optional[str] = ..., hashed_row_level_value: _Optional[str] = ..., clear_text_row_level_value: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., queries_count: _Optional[int] = ..., rows_count: _Optional[int] = ..., time_bucket: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RowLevelMetricConfiguration(_message.Message):
    __slots__ = ["datastore_id", "id", "metric_id", "path", "allow_clear_text_value", "created_at"]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    METRIC_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ALLOW_CLEAR_TEXT_VALUE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    datastore_id: str
    id: str
    metric_id: str
    path: str
    allow_clear_text_value: bool
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, datastore_id: _Optional[str] = ..., id: _Optional[str] = ..., metric_id: _Optional[str] = ..., path: _Optional[str] = ..., allow_clear_text_value: bool = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetCustomMetricsDetailsRequest(_message.Message):
    __slots__ = ["id", "interval", "user_id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    interval: str
    user_id: str
    def __init__(self, id: _Optional[str] = ..., interval: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class GetCustomMetricsDetailsResponse(_message.Message):
    __slots__ = ["series"]
    class SeriesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: MetricsGroup
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[MetricsGroup, _Mapping]] = ...) -> None: ...
    SERIES_FIELD_NUMBER: _ClassVar[int]
    series: _containers.MessageMap[str, MetricsGroup]
    def __init__(self, series: _Optional[_Mapping[str, MetricsGroup]] = ...) -> None: ...

class MetricsGroup(_message.Message):
    __slots__ = ["metrics", "clear_text"]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    CLEAR_TEXT_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[RowLevelMetric]
    clear_text: str
    def __init__(self, metrics: _Optional[_Iterable[_Union[RowLevelMetric, _Mapping]]] = ..., clear_text: _Optional[str] = ...) -> None: ...

class GetCustomMetricsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetCustomMetricsResponse(_message.Message):
    __slots__ = ["row_level_metric_configurations"]
    ROW_LEVEL_METRIC_CONFIGURATIONS_FIELD_NUMBER: _ClassVar[int]
    row_level_metric_configurations: _containers.RepeatedCompositeFieldContainer[RowLevelMetricConfiguration]
    def __init__(self, row_level_metric_configurations: _Optional[_Iterable[_Union[RowLevelMetricConfiguration, _Mapping]]] = ...) -> None: ...

class CreateCustomMetricRequest(_message.Message):
    __slots__ = ["datastore_id", "path", "allow_clear_text_value"]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ALLOW_CLEAR_TEXT_VALUE_FIELD_NUMBER: _ClassVar[int]
    datastore_id: str
    path: str
    allow_clear_text_value: bool
    def __init__(self, datastore_id: _Optional[str] = ..., path: _Optional[str] = ..., allow_clear_text_value: bool = ...) -> None: ...

class CreateCustomMetricResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteCustomMetricRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteCustomMetricResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
