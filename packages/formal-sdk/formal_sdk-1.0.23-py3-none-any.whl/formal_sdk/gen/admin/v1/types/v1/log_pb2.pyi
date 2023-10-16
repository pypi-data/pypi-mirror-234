from . import column_pb2 as _column_pb2
from . import domain_pb2 as _domain_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PolicyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    POLICY_TYPE_UNSPECIFIED: _ClassVar[PolicyType]
    POLICY_TYPE_FILTER_POLICY: _ClassVar[PolicyType]
    POLICY_TYPE_DECRYPTION_POLICY: _ClassVar[PolicyType]
    POLICY_TYPE_MASKING_POLICY: _ClassVar[PolicyType]
    POLICY_TYPE_BLOCK_POLICY: _ClassVar[PolicyType]
    POLICY_TYPE_ALLOW_POLICY: _ClassVar[PolicyType]
POLICY_TYPE_UNSPECIFIED: PolicyType
POLICY_TYPE_FILTER_POLICY: PolicyType
POLICY_TYPE_DECRYPTION_POLICY: PolicyType
POLICY_TYPE_MASKING_POLICY: PolicyType
POLICY_TYPE_BLOCK_POLICY: PolicyType
POLICY_TYPE_ALLOW_POLICY: PolicyType

class TriggeredPolicy(_message.Message):
    __slots__ = ["policy_id", "owners", "notify", "policy_type", "reason", "contextual_data"]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    OWNERS_FIELD_NUMBER: _ClassVar[int]
    NOTIFY_FIELD_NUMBER: _ClassVar[int]
    POLICY_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    CONTEXTUAL_DATA_FIELD_NUMBER: _ClassVar[int]
    policy_id: str
    owners: _containers.RepeatedScalarFieldContainer[str]
    notify: str
    policy_type: PolicyType
    reason: str
    contextual_data: str
    def __init__(self, policy_id: _Optional[str] = ..., owners: _Optional[_Iterable[str]] = ..., notify: _Optional[str] = ..., policy_type: _Optional[_Union[PolicyType, str]] = ..., reason: _Optional[str] = ..., contextual_data: _Optional[str] = ...) -> None: ...

class TriggeredFilterPolicy(_message.Message):
    __slots__ = ["interval", "limit", "count"]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    interval: str
    limit: int
    count: int
    def __init__(self, interval: _Optional[str] = ..., limit: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class TriggeredDecryptionPolicy(_message.Message):
    __slots__ = ["column_path"]
    COLUMN_PATH_FIELD_NUMBER: _ClassVar[int]
    column_path: str
    def __init__(self, column_path: _Optional[str] = ...) -> None: ...

class TriggeredMaskingPolicy(_message.Message):
    __slots__ = ["column_path", "masking_type", "typesafe"]
    COLUMN_PATH_FIELD_NUMBER: _ClassVar[int]
    MASKING_TYPE_FIELD_NUMBER: _ClassVar[int]
    TYPESAFE_FIELD_NUMBER: _ClassVar[int]
    column_path: str
    masking_type: str
    typesafe: bool
    def __init__(self, column_path: _Optional[str] = ..., masking_type: _Optional[str] = ..., typesafe: bool = ...) -> None: ...

class TriggeredBlockPolicy(_message.Message):
    __slots__ = ["object_type", "path", "object_paths", "multiple", "action", "datastore_is_default_block"]
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    OBJECT_PATHS_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_IS_DEFAULT_BLOCK_FIELD_NUMBER: _ClassVar[int]
    object_type: str
    path: str
    object_paths: _containers.RepeatedScalarFieldContainer[str]
    multiple: bool
    action: str
    datastore_is_default_block: bool
    def __init__(self, object_type: _Optional[str] = ..., path: _Optional[str] = ..., object_paths: _Optional[_Iterable[str]] = ..., multiple: bool = ..., action: _Optional[str] = ..., datastore_is_default_block: bool = ...) -> None: ...

class TiggeredAllowPolicy(_message.Message):
    __slots__ = ["object_type", "path"]
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    object_type: str
    path: str
    def __init__(self, object_type: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class LogRequest(_message.Message):
    __slots__ = ["start_time", "end_time", "sidecar_processing_time", "data_store_start_time", "data_store_end_time", "data_store_processing_time", "query", "success", "error_message", "stament_type", "returned_tables", "returned_columns", "data_volume", "end_user_id", "end_user_db_user_name", "end_user_external_ids", "policy_action", "returned_rows_count", "returned_rows_count_by_server", "returned_rows_count_to_user", "filtered_rows_count", "triggered_policies", "tenant_id", "row_level_metrics", "tenant_id_column_name", "tenant_mismatch", "bucket_name", "s3_action", "returned_objects", "ssh_aws_connection_type", "ssh_aws_arn", "end_user_groups", "user_groups", "groups", "fingerprint", "data_domains", "request_body", "response_body", "request_body_encrypted", "response_body_encrypted"]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    SIDECAR_PROCESSING_TIME_FIELD_NUMBER: _ClassVar[int]
    DATA_STORE_START_TIME_FIELD_NUMBER: _ClassVar[int]
    DATA_STORE_END_TIME_FIELD_NUMBER: _ClassVar[int]
    DATA_STORE_PROCESSING_TIME_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STAMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    RETURNED_TABLES_FIELD_NUMBER: _ClassVar[int]
    RETURNED_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    DATA_VOLUME_FIELD_NUMBER: _ClassVar[int]
    END_USER_ID_FIELD_NUMBER: _ClassVar[int]
    END_USER_DB_USER_NAME_FIELD_NUMBER: _ClassVar[int]
    END_USER_EXTERNAL_IDS_FIELD_NUMBER: _ClassVar[int]
    POLICY_ACTION_FIELD_NUMBER: _ClassVar[int]
    RETURNED_ROWS_COUNT_FIELD_NUMBER: _ClassVar[int]
    RETURNED_ROWS_COUNT_BY_SERVER_FIELD_NUMBER: _ClassVar[int]
    RETURNED_ROWS_COUNT_TO_USER_FIELD_NUMBER: _ClassVar[int]
    FILTERED_ROWS_COUNT_FIELD_NUMBER: _ClassVar[int]
    TRIGGERED_POLICIES_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    ROW_LEVEL_METRICS_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    TENANT_MISMATCH_FIELD_NUMBER: _ClassVar[int]
    BUCKET_NAME_FIELD_NUMBER: _ClassVar[int]
    S3_ACTION_FIELD_NUMBER: _ClassVar[int]
    RETURNED_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    SSH_AWS_CONNECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    SSH_AWS_ARN_FIELD_NUMBER: _ClassVar[int]
    END_USER_GROUPS_FIELD_NUMBER: _ClassVar[int]
    USER_GROUPS_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    DATA_DOMAINS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_BODY_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_BODY_FIELD_NUMBER: _ClassVar[int]
    REQUEST_BODY_ENCRYPTED_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_BODY_ENCRYPTED_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    sidecar_processing_time: _duration_pb2.Duration
    data_store_start_time: _timestamp_pb2.Timestamp
    data_store_end_time: _timestamp_pb2.Timestamp
    data_store_processing_time: _duration_pb2.Duration
    query: str
    success: bool
    error_message: str
    stament_type: str
    returned_tables: _containers.RepeatedScalarFieldContainer[str]
    returned_columns: _containers.RepeatedCompositeFieldContainer[_column_pb2.Column]
    data_volume: int
    end_user_id: str
    end_user_db_user_name: str
    end_user_external_ids: _containers.RepeatedScalarFieldContainer[str]
    policy_action: str
    returned_rows_count: int
    returned_rows_count_by_server: int
    returned_rows_count_to_user: int
    filtered_rows_count: int
    triggered_policies: _containers.RepeatedCompositeFieldContainer[TriggeredPolicy]
    tenant_id: str
    row_level_metrics: _containers.RepeatedCompositeFieldContainer[RowLevelMetric]
    tenant_id_column_name: str
    tenant_mismatch: _containers.RepeatedScalarFieldContainer[str]
    bucket_name: str
    s3_action: str
    returned_objects: _containers.RepeatedCompositeFieldContainer[S3Object]
    ssh_aws_connection_type: str
    ssh_aws_arn: str
    end_user_groups: _containers.RepeatedScalarFieldContainer[str]
    user_groups: _containers.RepeatedScalarFieldContainer[str]
    groups: _containers.RepeatedScalarFieldContainer[str]
    fingerprint: str
    data_domains: _containers.RepeatedCompositeFieldContainer[_domain_pb2.Domain]
    request_body: str
    response_body: str
    request_body_encrypted: bool
    response_body_encrypted: bool
    def __init__(self, start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., sidecar_processing_time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., data_store_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., data_store_end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., data_store_processing_time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., query: _Optional[str] = ..., success: bool = ..., error_message: _Optional[str] = ..., stament_type: _Optional[str] = ..., returned_tables: _Optional[_Iterable[str]] = ..., returned_columns: _Optional[_Iterable[_Union[_column_pb2.Column, _Mapping]]] = ..., data_volume: _Optional[int] = ..., end_user_id: _Optional[str] = ..., end_user_db_user_name: _Optional[str] = ..., end_user_external_ids: _Optional[_Iterable[str]] = ..., policy_action: _Optional[str] = ..., returned_rows_count: _Optional[int] = ..., returned_rows_count_by_server: _Optional[int] = ..., returned_rows_count_to_user: _Optional[int] = ..., filtered_rows_count: _Optional[int] = ..., triggered_policies: _Optional[_Iterable[_Union[TriggeredPolicy, _Mapping]]] = ..., tenant_id: _Optional[str] = ..., row_level_metrics: _Optional[_Iterable[_Union[RowLevelMetric, _Mapping]]] = ..., tenant_id_column_name: _Optional[str] = ..., tenant_mismatch: _Optional[_Iterable[str]] = ..., bucket_name: _Optional[str] = ..., s3_action: _Optional[str] = ..., returned_objects: _Optional[_Iterable[_Union[S3Object, _Mapping]]] = ..., ssh_aws_connection_type: _Optional[str] = ..., ssh_aws_arn: _Optional[str] = ..., end_user_groups: _Optional[_Iterable[str]] = ..., user_groups: _Optional[_Iterable[str]] = ..., groups: _Optional[_Iterable[str]] = ..., fingerprint: _Optional[str] = ..., data_domains: _Optional[_Iterable[_Union[_domain_pb2.Domain, _Mapping]]] = ..., request_body: _Optional[str] = ..., response_body: _Optional[str] = ..., request_body_encrypted: bool = ..., response_body_encrypted: bool = ...) -> None: ...

class Session(_message.Message):
    __slots__ = ["id", "start_time", "datastore_id", "datastore_name", "datastore_technology", "datastore_deployment_type", "server_ip_address", "client_ip_address", "user_id", "user_type", "db_user", "db_name", "application_name", "schemas", "native_role_id", "native_role_assignment", "sidecar_id", "sidecar_name", "sidecar_technology", "aws_account_id", "aws_region", "aws_ec2_instance_id", "aws_ecs_cluster_name", "aws_ecs_cluster_arn", "aws_ecs_service_name", "aws_ecs_service_arn", "aws_ecs_task_id", "aws_ecs_task_arn", "container_name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_NAME_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_TECHNOLOGY_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_DEPLOYMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SERVER_IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_TYPE_FIELD_NUMBER: _ClassVar[int]
    DB_USER_FIELD_NUMBER: _ClassVar[int]
    DB_NAME_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEMAS_FIELD_NUMBER: _ClassVar[int]
    NATIVE_ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    NATIVE_ROLE_ASSIGNMENT_FIELD_NUMBER: _ClassVar[int]
    SIDECAR_ID_FIELD_NUMBER: _ClassVar[int]
    SIDECAR_NAME_FIELD_NUMBER: _ClassVar[int]
    SIDECAR_TECHNOLOGY_FIELD_NUMBER: _ClassVar[int]
    AWS_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    AWS_REGION_FIELD_NUMBER: _ClassVar[int]
    AWS_EC2_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    AWS_ECS_CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    AWS_ECS_CLUSTER_ARN_FIELD_NUMBER: _ClassVar[int]
    AWS_ECS_SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    AWS_ECS_SERVICE_ARN_FIELD_NUMBER: _ClassVar[int]
    AWS_ECS_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    AWS_ECS_TASK_ARN_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    start_time: int
    datastore_id: str
    datastore_name: str
    datastore_technology: str
    datastore_deployment_type: str
    server_ip_address: str
    client_ip_address: str
    user_id: str
    user_type: str
    db_user: str
    db_name: str
    application_name: str
    schemas: _containers.RepeatedScalarFieldContainer[str]
    native_role_id: str
    native_role_assignment: str
    sidecar_id: str
    sidecar_name: str
    sidecar_technology: str
    aws_account_id: str
    aws_region: str
    aws_ec2_instance_id: str
    aws_ecs_cluster_name: str
    aws_ecs_cluster_arn: str
    aws_ecs_service_name: str
    aws_ecs_service_arn: str
    aws_ecs_task_id: str
    aws_ecs_task_arn: str
    container_name: str
    def __init__(self, id: _Optional[str] = ..., start_time: _Optional[int] = ..., datastore_id: _Optional[str] = ..., datastore_name: _Optional[str] = ..., datastore_technology: _Optional[str] = ..., datastore_deployment_type: _Optional[str] = ..., server_ip_address: _Optional[str] = ..., client_ip_address: _Optional[str] = ..., user_id: _Optional[str] = ..., user_type: _Optional[str] = ..., db_user: _Optional[str] = ..., db_name: _Optional[str] = ..., application_name: _Optional[str] = ..., schemas: _Optional[_Iterable[str]] = ..., native_role_id: _Optional[str] = ..., native_role_assignment: _Optional[str] = ..., sidecar_id: _Optional[str] = ..., sidecar_name: _Optional[str] = ..., sidecar_technology: _Optional[str] = ..., aws_account_id: _Optional[str] = ..., aws_region: _Optional[str] = ..., aws_ec2_instance_id: _Optional[str] = ..., aws_ecs_cluster_name: _Optional[str] = ..., aws_ecs_cluster_arn: _Optional[str] = ..., aws_ecs_service_name: _Optional[str] = ..., aws_ecs_service_arn: _Optional[str] = ..., aws_ecs_task_id: _Optional[str] = ..., aws_ecs_task_arn: _Optional[str] = ..., container_name: _Optional[str] = ...) -> None: ...

class FormalLog(_message.Message):
    __slots__ = ["id", "datastore_id", "session", "request", "created_at", "timestamp", "total"]
    ID_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    id: str
    datastore_id: str
    session: Session
    request: LogRequest
    created_at: str
    timestamp: _timestamp_pb2.Timestamp
    total: int
    def __init__(self, id: _Optional[str] = ..., datastore_id: _Optional[str] = ..., session: _Optional[_Union[Session, _Mapping]] = ..., request: _Optional[_Union[LogRequest, _Mapping]] = ..., created_at: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., total: _Optional[int] = ...) -> None: ...

class TenantLogsInfra(_message.Message):
    __slots__ = ["uri", "password", "username", "metrics_role_pwd"]
    URI_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    METRICS_ROLE_PWD_FIELD_NUMBER: _ClassVar[int]
    uri: str
    password: str
    username: str
    metrics_role_pwd: str
    def __init__(self, uri: _Optional[str] = ..., password: _Optional[str] = ..., username: _Optional[str] = ..., metrics_role_pwd: _Optional[str] = ...) -> None: ...

class LogStorageS3(_message.Message):
    __slots__ = ["s3_firehose_stream_arn"]
    S3_FIREHOSE_STREAM_ARN_FIELD_NUMBER: _ClassVar[int]
    s3_firehose_stream_arn: str
    def __init__(self, s3_firehose_stream_arn: _Optional[str] = ...) -> None: ...

class CsvOrParquetColumn(_message.Message):
    __slots__ = ["col_index", "name", "data_type"]
    COL_INDEX_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    col_index: int
    name: str
    data_type: str
    def __init__(self, col_index: _Optional[int] = ..., name: _Optional[str] = ..., data_type: _Optional[str] = ...) -> None: ...

class Image(_message.Message):
    __slots__ = ["name", "faces_count", "width", "height", "type", "policy_action"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FACES_COUNT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    POLICY_ACTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    faces_count: int
    width: int
    height: int
    type: str
    policy_action: str
    def __init__(self, name: _Optional[str] = ..., faces_count: _Optional[int] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., type: _Optional[str] = ..., policy_action: _Optional[str] = ...) -> None: ...

class S3Object(_message.Message):
    __slots__ = ["name", "content_type", "content_length", "columns", "image"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_LENGTH_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    name: str
    content_type: str
    content_length: int
    columns: _containers.RepeatedCompositeFieldContainer[CsvOrParquetColumn]
    image: Image
    def __init__(self, name: _Optional[str] = ..., content_type: _Optional[str] = ..., content_length: _Optional[int] = ..., columns: _Optional[_Iterable[_Union[CsvOrParquetColumn, _Mapping]]] = ..., image: _Optional[_Union[Image, _Mapping]] = ...) -> None: ...

class RowLevelMetric(_message.Message):
    __slots__ = ["datastore_id", "datastore_name", "end_user_id", "end_user_db_username", "user_id", "db_user", "db_name", "schema_name", "table_name", "path", "hashed_row_level_value", "clear_text_row_level_value", "ts", "counter", "returned_rows", "timebucket"]
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
    TS_FIELD_NUMBER: _ClassVar[int]
    COUNTER_FIELD_NUMBER: _ClassVar[int]
    RETURNED_ROWS_FIELD_NUMBER: _ClassVar[int]
    TIMEBUCKET_FIELD_NUMBER: _ClassVar[int]
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
    ts: _timestamp_pb2.Timestamp
    counter: int
    returned_rows: int
    timebucket: _timestamp_pb2.Timestamp
    def __init__(self, datastore_id: _Optional[str] = ..., datastore_name: _Optional[str] = ..., end_user_id: _Optional[str] = ..., end_user_db_username: _Optional[str] = ..., user_id: _Optional[str] = ..., db_user: _Optional[str] = ..., db_name: _Optional[str] = ..., schema_name: _Optional[str] = ..., table_name: _Optional[str] = ..., path: _Optional[str] = ..., hashed_row_level_value: _Optional[str] = ..., clear_text_row_level_value: _Optional[str] = ..., ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., counter: _Optional[int] = ..., returned_rows: _Optional[int] = ..., timebucket: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
