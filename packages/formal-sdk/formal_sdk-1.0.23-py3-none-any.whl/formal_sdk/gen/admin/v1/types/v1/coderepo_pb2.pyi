from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CodeRepo(_message.Message):
    __slots__ = ["id", "cloud_provider_repo_id", "created_by", "type", "name", "hook_id", "status", "active", "created_at", "updated_at", "expire_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_PROVIDER_REPO_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    HOOK_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    cloud_provider_repo_id: int
    created_by: str
    type: str
    name: str
    hook_id: int
    status: str
    active: bool
    created_at: str
    updated_at: str
    expire_at: str
    def __init__(self, id: _Optional[str] = ..., cloud_provider_repo_id: _Optional[int] = ..., created_by: _Optional[str] = ..., type: _Optional[str] = ..., name: _Optional[str] = ..., hook_id: _Optional[int] = ..., status: _Optional[str] = ..., active: bool = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., expire_at: _Optional[str] = ...) -> None: ...
