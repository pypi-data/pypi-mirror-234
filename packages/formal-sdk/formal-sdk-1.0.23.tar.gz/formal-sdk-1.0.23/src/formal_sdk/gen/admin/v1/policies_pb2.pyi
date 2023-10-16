from google.protobuf import any_pb2 as _any_pb2
from .types.v1 import policy_pb2 as _policy_pb2
from .types.v1 import list_metadata_pb2 as _list_metadata_pb2
from ...validate.v1 import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PolicyRuleType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    POLICY_RULE_TYPE_UNSPECIFIED: _ClassVar[PolicyRuleType]
    POLICY_RULE_TYPE_SESSION: _ClassVar[PolicyRuleType]
    POLICY_RULE_TYPE_PRE: _ClassVar[PolicyRuleType]
    POLICY_RULE_TYPE_POST: _ClassVar[PolicyRuleType]

class PolicyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    POLICY_TYPE_UNSPECIFIED: _ClassVar[PolicyType]
    POLICY_TYPE_ALLOW: _ClassVar[PolicyType]
    POLICY_TYPE_BLOCK: _ClassVar[PolicyType]
    POLICY_TYPE_REWRITE: _ClassVar[PolicyType]
    POLICY_TYPE_ENCRYPT: _ClassVar[PolicyType]
    POLICY_TYPE_DECRYPT: _ClassVar[PolicyType]
    POLICY_TYPE_MASK: _ClassVar[PolicyType]
POLICY_RULE_TYPE_UNSPECIFIED: PolicyRuleType
POLICY_RULE_TYPE_SESSION: PolicyRuleType
POLICY_RULE_TYPE_PRE: PolicyRuleType
POLICY_RULE_TYPE_POST: PolicyRuleType
POLICY_TYPE_UNSPECIFIED: PolicyType
POLICY_TYPE_ALLOW: PolicyType
POLICY_TYPE_BLOCK: PolicyType
POLICY_TYPE_REWRITE: PolicyType
POLICY_TYPE_ENCRYPT: PolicyType
POLICY_TYPE_DECRYPT: PolicyType
POLICY_TYPE_MASK: PolicyType

class CreatePolicySuggestionRequest(_message.Message):
    __slots__ = ["name", "description"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreatePolicySuggestionResponse(_message.Message):
    __slots__ = ["suggestion"]
    SUGGESTION_FIELD_NUMBER: _ClassVar[int]
    suggestion: str
    def __init__(self, suggestion: _Optional[str] = ...) -> None: ...

class DeletePolicyRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeletePolicyResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class EvaluatePolicyValidityRequest(_message.Message):
    __slots__ = ["code"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: str
    def __init__(self, code: _Optional[str] = ...) -> None: ...

class EvaluatePolicyValidityResponse(_message.Message):
    __slots__ = ["valid", "ast", "error"]
    VALID_FIELD_NUMBER: _ClassVar[int]
    AST_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    ast: str
    error: str
    def __init__(self, valid: bool = ..., ast: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class DryRunPoliciesRequest(_message.Message):
    __slots__ = ["policy_rule_type", "application_name", "client_ip_address", "client_tls", "statement_type", "db_name", "schema_paths", "table_paths", "column_tags", "column_name", "column_path", "data_label", "sidecar_id", "aws", "columns", "user_id"]
    POLICY_RULE_TYPE_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_NAME_FIELD_NUMBER: _ClassVar[int]
    CLIENT_IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TLS_FIELD_NUMBER: _ClassVar[int]
    STATEMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    DB_NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_PATHS_FIELD_NUMBER: _ClassVar[int]
    TABLE_PATHS_FIELD_NUMBER: _ClassVar[int]
    COLUMN_TAGS_FIELD_NUMBER: _ClassVar[int]
    COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    COLUMN_PATH_FIELD_NUMBER: _ClassVar[int]
    DATA_LABEL_FIELD_NUMBER: _ClassVar[int]
    SIDECAR_ID_FIELD_NUMBER: _ClassVar[int]
    AWS_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    policy_rule_type: PolicyRuleType
    application_name: str
    client_ip_address: str
    client_tls: bool
    statement_type: str
    db_name: str
    schema_paths: _containers.RepeatedScalarFieldContainer[str]
    table_paths: _containers.RepeatedScalarFieldContainer[str]
    column_tags: _containers.RepeatedScalarFieldContainer[str]
    column_name: str
    column_path: str
    data_label: str
    sidecar_id: str
    aws: AWS
    columns: _containers.RepeatedCompositeFieldContainer[ColumnPolicy]
    user_id: str
    def __init__(self, policy_rule_type: _Optional[_Union[PolicyRuleType, str]] = ..., application_name: _Optional[str] = ..., client_ip_address: _Optional[str] = ..., client_tls: bool = ..., statement_type: _Optional[str] = ..., db_name: _Optional[str] = ..., schema_paths: _Optional[_Iterable[str]] = ..., table_paths: _Optional[_Iterable[str]] = ..., column_tags: _Optional[_Iterable[str]] = ..., column_name: _Optional[str] = ..., column_path: _Optional[str] = ..., data_label: _Optional[str] = ..., sidecar_id: _Optional[str] = ..., aws: _Optional[_Union[AWS, _Mapping]] = ..., columns: _Optional[_Iterable[_Union[ColumnPolicy, _Mapping]]] = ..., user_id: _Optional[str] = ...) -> None: ...

class ColumnPolicy(_message.Message):
    __slots__ = ["index", "parent_column_path", "parent_column_type", "parent_is_array", "parent_index", "parent_data_type", "sub_column", "data_type", "name", "path", "tags", "data_label", "value", "row_level_usage", "array_index", "json_path"]
    class RowLevelUsageEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    INDEX_FIELD_NUMBER: _ClassVar[int]
    PARENT_COLUMN_PATH_FIELD_NUMBER: _ClassVar[int]
    PARENT_COLUMN_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARENT_IS_ARRAY_FIELD_NUMBER: _ClassVar[int]
    PARENT_INDEX_FIELD_NUMBER: _ClassVar[int]
    PARENT_DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_COLUMN_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DATA_LABEL_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ROW_LEVEL_USAGE_FIELD_NUMBER: _ClassVar[int]
    ARRAY_INDEX_FIELD_NUMBER: _ClassVar[int]
    JSON_PATH_FIELD_NUMBER: _ClassVar[int]
    index: int
    parent_column_path: str
    parent_column_type: str
    parent_is_array: bool
    parent_index: int
    parent_data_type: str
    sub_column: bool
    data_type: str
    name: str
    path: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    data_label: str
    value: _any_pb2.Any
    row_level_usage: _containers.ScalarMap[str, int]
    array_index: int
    json_path: str
    def __init__(self, index: _Optional[int] = ..., parent_column_path: _Optional[str] = ..., parent_column_type: _Optional[str] = ..., parent_is_array: bool = ..., parent_index: _Optional[int] = ..., parent_data_type: _Optional[str] = ..., sub_column: bool = ..., data_type: _Optional[str] = ..., name: _Optional[str] = ..., path: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., data_label: _Optional[str] = ..., value: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., row_level_usage: _Optional[_Mapping[str, int]] = ..., array_index: _Optional[int] = ..., json_path: _Optional[str] = ...) -> None: ...

class AWSAccount(_message.Message):
    __slots__ = ["account_id", "region"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    region: str
    def __init__(self, account_id: _Optional[str] = ..., region: _Optional[str] = ...) -> None: ...

class AWSEC2(_message.Message):
    __slots__ = ["instance_id"]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    instance_id: str
    def __init__(self, instance_id: _Optional[str] = ...) -> None: ...

class AWSECS(_message.Message):
    __slots__ = ["cluster_name", "service_name", "task_id", "container_name"]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_NAME_FIELD_NUMBER: _ClassVar[int]
    cluster_name: str
    service_name: str
    task_id: str
    container_name: str
    def __init__(self, cluster_name: _Optional[str] = ..., service_name: _Optional[str] = ..., task_id: _Optional[str] = ..., container_name: _Optional[str] = ...) -> None: ...

class AWS(_message.Message):
    __slots__ = ["account", "ec2", "ecs"]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    EC2_FIELD_NUMBER: _ClassVar[int]
    ECS_FIELD_NUMBER: _ClassVar[int]
    account: AWSAccount
    ec2: AWSEC2
    ecs: AWSECS
    def __init__(self, account: _Optional[_Union[AWSAccount, _Mapping]] = ..., ec2: _Optional[_Union[AWSEC2, _Mapping]] = ..., ecs: _Optional[_Union[AWSECS, _Mapping]] = ...) -> None: ...

class DryRunPoliciesResponse(_message.Message):
    __slots__ = ["results"]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedScalarFieldContainer[PolicyType]
    def __init__(self, results: _Optional[_Iterable[_Union[PolicyType, str]]] = ...) -> None: ...

class CreatePolicyRequest(_message.Message):
    __slots__ = ["name", "description", "code", "notification", "owners", "source_type", "active"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    OWNERS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    code: str
    notification: str
    owners: _containers.RepeatedScalarFieldContainer[str]
    source_type: str
    active: bool
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., code: _Optional[str] = ..., notification: _Optional[str] = ..., owners: _Optional[_Iterable[str]] = ..., source_type: _Optional[str] = ..., active: bool = ...) -> None: ...

class CreatePolicyV2Request(_message.Message):
    __slots__ = ["name", "description", "code", "notification", "owners", "source_type", "active", "status"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    OWNERS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    code: str
    notification: str
    owners: _containers.RepeatedScalarFieldContainer[str]
    source_type: str
    active: bool
    status: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., code: _Optional[str] = ..., notification: _Optional[str] = ..., owners: _Optional[_Iterable[str]] = ..., source_type: _Optional[str] = ..., active: bool = ..., status: _Optional[str] = ...) -> None: ...

class CreatePolicyResponse(_message.Message):
    __slots__ = ["policy"]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: _policy_pb2.Policy
    def __init__(self, policy: _Optional[_Union[_policy_pb2.Policy, _Mapping]] = ...) -> None: ...

class CreatePolicyV2Response(_message.Message):
    __slots__ = ["policy"]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: _policy_pb2.PolicyV2
    def __init__(self, policy: _Optional[_Union[_policy_pb2.PolicyV2, _Mapping]] = ...) -> None: ...

class UpdatePolicyRequest(_message.Message):
    __slots__ = ["id", "source_type", "name", "description", "code", "notification", "owners", "active"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    OWNERS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    id: str
    source_type: str
    name: str
    description: str
    code: str
    notification: str
    owners: _containers.RepeatedScalarFieldContainer[str]
    active: bool
    def __init__(self, id: _Optional[str] = ..., source_type: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., code: _Optional[str] = ..., notification: _Optional[str] = ..., owners: _Optional[_Iterable[str]] = ..., active: bool = ...) -> None: ...

class UpdatePolicyV2Request(_message.Message):
    __slots__ = ["id", "source_type", "name", "description", "code", "notification", "owners", "active", "status"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    OWNERS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    source_type: str
    name: str
    description: str
    code: str
    notification: str
    owners: _containers.RepeatedScalarFieldContainer[str]
    active: bool
    status: str
    def __init__(self, id: _Optional[str] = ..., source_type: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., code: _Optional[str] = ..., notification: _Optional[str] = ..., owners: _Optional[_Iterable[str]] = ..., active: bool = ..., status: _Optional[str] = ...) -> None: ...

class UpdatePolicyResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UpdatePolicyV2Response(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetPolicyRequest(_message.Message):
    __slots__ = ["policy_id"]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    policy_id: str
    def __init__(self, policy_id: _Optional[str] = ...) -> None: ...

class GetPolicyV2Request(_message.Message):
    __slots__ = ["policy_id"]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    policy_id: str
    def __init__(self, policy_id: _Optional[str] = ...) -> None: ...

class GetPolicyResponse(_message.Message):
    __slots__ = ["policy"]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: _policy_pb2.Policy
    def __init__(self, policy: _Optional[_Union[_policy_pb2.Policy, _Mapping]] = ...) -> None: ...

class GetPolicyV2Response(_message.Message):
    __slots__ = ["policy"]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: _policy_pb2.PolicyV2
    def __init__(self, policy: _Optional[_Union[_policy_pb2.PolicyV2, _Mapping]] = ...) -> None: ...

class GetPoliciesRequest(_message.Message):
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

class GetPoliciesResponse(_message.Message):
    __slots__ = ["policies", "list_metadata"]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    LIST_METADATA_FIELD_NUMBER: _ClassVar[int]
    policies: _containers.RepeatedCompositeFieldContainer[_policy_pb2.Policy]
    list_metadata: _list_metadata_pb2.ListMetadata
    def __init__(self, policies: _Optional[_Iterable[_Union[_policy_pb2.Policy, _Mapping]]] = ..., list_metadata: _Optional[_Union[_list_metadata_pb2.ListMetadata, _Mapping]] = ...) -> None: ...
