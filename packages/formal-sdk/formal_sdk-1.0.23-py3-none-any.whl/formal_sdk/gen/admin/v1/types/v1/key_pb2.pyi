from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Key(_message.Message):
    __slots__ = ["id", "cloud_region", "key_id", "key_arn", "active", "managed_by", "key_type", "name", "cloud_account_id", "created_at", "updated_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_REGION_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_ARN_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    MANAGED_BY_FIELD_NUMBER: _ClassVar[int]
    KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CLOUD_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    cloud_region: str
    key_id: str
    key_arn: str
    active: bool
    managed_by: str
    key_type: str
    name: str
    cloud_account_id: str
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., cloud_region: _Optional[str] = ..., key_id: _Optional[str] = ..., key_arn: _Optional[str] = ..., active: bool = ..., managed_by: _Optional[str] = ..., key_type: _Optional[str] = ..., name: _Optional[str] = ..., cloud_account_id: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...
