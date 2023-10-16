from . import external_id_pb2 as _external_id_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ["id", "organization_id", "first_name", "last_name", "type", "app_type", "role", "name", "db_username", "email", "idp", "idp_user_id", "status", "expire_at", "created_at", "external_ids", "machine_role_access_token", "dsync_user_id", "app_id", "admin"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    APP_TYPE_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DB_USERNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    IDP_FIELD_NUMBER: _ClassVar[int]
    IDP_USER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_IDS_FIELD_NUMBER: _ClassVar[int]
    MACHINE_ROLE_ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    DSYNC_USER_ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    ADMIN_FIELD_NUMBER: _ClassVar[int]
    id: str
    organization_id: str
    first_name: str
    last_name: str
    type: str
    app_type: str
    role: str
    name: str
    db_username: str
    email: str
    idp: str
    idp_user_id: str
    status: str
    expire_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    external_ids: _containers.RepeatedCompositeFieldContainer[_external_id_pb2.ExternalId]
    machine_role_access_token: str
    dsync_user_id: str
    app_id: str
    admin: bool
    def __init__(self, id: _Optional[str] = ..., organization_id: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., type: _Optional[str] = ..., app_type: _Optional[str] = ..., role: _Optional[str] = ..., name: _Optional[str] = ..., db_username: _Optional[str] = ..., email: _Optional[str] = ..., idp: _Optional[str] = ..., idp_user_id: _Optional[str] = ..., status: _Optional[str] = ..., expire_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., external_ids: _Optional[_Iterable[_Union[_external_id_pb2.ExternalId, _Mapping]]] = ..., machine_role_access_token: _Optional[str] = ..., dsync_user_id: _Optional[str] = ..., app_id: _Optional[str] = ..., admin: bool = ...) -> None: ...
