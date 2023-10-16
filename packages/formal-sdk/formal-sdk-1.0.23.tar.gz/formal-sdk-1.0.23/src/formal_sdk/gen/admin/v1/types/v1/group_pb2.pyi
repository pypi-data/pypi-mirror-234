from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Group(_message.Message):
    __slots__ = ["id", "name", "description", "active", "status", "roles", "created_at", "user_ids", "dsync_group_id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    DSYNC_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    active: bool
    status: str
    roles: _containers.RepeatedCompositeFieldContainer[DbUser]
    created_at: _timestamp_pb2.Timestamp
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    dsync_group_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., active: bool = ..., status: _Optional[str] = ..., roles: _Optional[_Iterable[_Union[DbUser, _Mapping]]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., user_ids: _Optional[_Iterable[str]] = ..., dsync_group_id: _Optional[str] = ...) -> None: ...

class DbUser(_message.Message):
    __slots__ = ["id", "db_username", "active", "status", "type", "expire_at", "created_at", "updated_at", "dsync_user_id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    DB_USERNAME_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DSYNC_USER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    db_username: str
    active: bool
    status: str
    type: str
    expire_at: int
    created_at: int
    updated_at: int
    dsync_user_id: str
    def __init__(self, id: _Optional[str] = ..., db_username: _Optional[str] = ..., active: bool = ..., status: _Optional[str] = ..., type: _Optional[str] = ..., expire_at: _Optional[int] = ..., created_at: _Optional[int] = ..., updated_at: _Optional[int] = ..., dsync_user_id: _Optional[str] = ...) -> None: ...
