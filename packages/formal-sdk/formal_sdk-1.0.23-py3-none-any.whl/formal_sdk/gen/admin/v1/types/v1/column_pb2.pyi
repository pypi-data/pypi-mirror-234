from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Column(_message.Message):
    __slots__ = ["created_at", "updated_at", "datastore_id", "datastore_name", "path", "table_physical_id", "table_attribute_number", "name", "alias", "table_path", "data_label", "data_type", "data_type_oid", "data_label_locked_for_sidecar", "tags", "encrypted", "policy_action", "decrypted_at_query_time", "decryption_policy_id", "data_domain_ids"]
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
    POLICY_ACTION_FIELD_NUMBER: _ClassVar[int]
    DECRYPTED_AT_QUERY_TIME_FIELD_NUMBER: _ClassVar[int]
    DECRYPTION_POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_DOMAIN_IDS_FIELD_NUMBER: _ClassVar[int]
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
    policy_action: str
    decrypted_at_query_time: bool
    decryption_policy_id: str
    data_domain_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, created_at: _Optional[int] = ..., updated_at: _Optional[int] = ..., datastore_id: _Optional[str] = ..., datastore_name: _Optional[str] = ..., path: _Optional[str] = ..., table_physical_id: _Optional[str] = ..., table_attribute_number: _Optional[int] = ..., name: _Optional[str] = ..., alias: _Optional[str] = ..., table_path: _Optional[str] = ..., data_label: _Optional[str] = ..., data_type: _Optional[str] = ..., data_type_oid: _Optional[int] = ..., data_label_locked_for_sidecar: bool = ..., tags: _Optional[_Iterable[str]] = ..., encrypted: bool = ..., policy_action: _Optional[str] = ..., decrypted_at_query_time: bool = ..., decryption_policy_id: _Optional[str] = ..., data_domain_ids: _Optional[_Iterable[str]] = ...) -> None: ...
