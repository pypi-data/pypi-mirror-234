from .types.v1 import external_id_pb2 as _external_id_pb2
from .types.v1 import group_pb2 as _group_pb2
from .types.v1 import user_pb2 as _user_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from .types.v1 import list_metadata_pb2 as _list_metadata_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListGroupsRequest(_message.Message):
    __slots__ = ["limit", "cursor", "order"]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    order: str
    def __init__(self, limit: _Optional[int] = ..., cursor: _Optional[str] = ..., order: _Optional[str] = ...) -> None: ...

class CreateGroupRequest(_message.Message):
    __slots__ = ["name", "description"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class GetGroupByIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteGroupRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class UpdateGroupRequest(_message.Message):
    __slots__ = ["id", "name", "description"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class LinkUsersToGroupRequest(_message.Message):
    __slots__ = ["id", "user_ids"]
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., user_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class LinkUsersToGroupV2Request(_message.Message):
    __slots__ = ["id", "user_ids"]
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., user_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class UnlinkUsersFromGroupRequest(_message.Message):
    __slots__ = ["id", "user_ids"]
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., user_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateGroupResponse(_message.Message):
    __slots__ = ["group"]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: _group_pb2.Group
    def __init__(self, group: _Optional[_Union[_group_pb2.Group, _Mapping]] = ...) -> None: ...

class GetGroupByIdResponse(_message.Message):
    __slots__ = ["group"]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: _group_pb2.Group
    def __init__(self, group: _Optional[_Union[_group_pb2.Group, _Mapping]] = ...) -> None: ...

class DeleteGroupResponse(_message.Message):
    __slots__ = ["group"]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: _group_pb2.Group
    def __init__(self, group: _Optional[_Union[_group_pb2.Group, _Mapping]] = ...) -> None: ...

class UpdateGroupResponse(_message.Message):
    __slots__ = ["group"]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: _group_pb2.Group
    def __init__(self, group: _Optional[_Union[_group_pb2.Group, _Mapping]] = ...) -> None: ...

class ListGroupsResponse(_message.Message):
    __slots__ = ["groups", "list_metadata"]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    LIST_METADATA_FIELD_NUMBER: _ClassVar[int]
    groups: _containers.RepeatedCompositeFieldContainer[_group_pb2.Group]
    list_metadata: _list_metadata_pb2.ListMetadata
    def __init__(self, groups: _Optional[_Iterable[_Union[_group_pb2.Group, _Mapping]]] = ..., list_metadata: _Optional[_Union[_list_metadata_pb2.ListMetadata, _Mapping]] = ...) -> None: ...

class LinkUsersToGroupResponse(_message.Message):
    __slots__ = ["user_ids", "group_id"]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    group_id: str
    def __init__(self, user_ids: _Optional[_Iterable[str]] = ..., group_id: _Optional[str] = ...) -> None: ...

class LinkUsersToGroupV2Response(_message.Message):
    __slots__ = ["user_ids", "group_id"]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    group_id: str
    def __init__(self, user_ids: _Optional[_Iterable[str]] = ..., group_id: _Optional[str] = ...) -> None: ...

class UnlinkUsersFromGroupResponse(_message.Message):
    __slots__ = ["user_ids", "group_id"]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    group_id: str
    def __init__(self, user_ids: _Optional[_Iterable[str]] = ..., group_id: _Optional[str] = ...) -> None: ...

class UserLinkGroupResponse(_message.Message):
    __slots__ = ["user_ids", "group_id"]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    group_id: str
    def __init__(self, user_ids: _Optional[_Iterable[str]] = ..., group_id: _Optional[str] = ...) -> None: ...

class ListUsersRequest(_message.Message):
    __slots__ = ["limit", "cursor", "order"]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    order: str
    def __init__(self, limit: _Optional[int] = ..., cursor: _Optional[str] = ..., order: _Optional[str] = ...) -> None: ...

class ListUsersResponse(_message.Message):
    __slots__ = ["users", "list_metadata"]
    USERS_FIELD_NUMBER: _ClassVar[int]
    LIST_METADATA_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[_user_pb2.User]
    list_metadata: _list_metadata_pb2.ListMetadata
    def __init__(self, users: _Optional[_Iterable[_Union[_user_pb2.User, _Mapping]]] = ..., list_metadata: _Optional[_Union[_list_metadata_pb2.ListMetadata, _Mapping]] = ...) -> None: ...

class CreateUserRequest(_message.Message):
    __slots__ = ["first_name", "last_name", "type", "app_type", "app_id", "name", "email", "admin", "idp", "status", "expire_at"]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    APP_TYPE_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ADMIN_FIELD_NUMBER: _ClassVar[int]
    IDP_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_AT_FIELD_NUMBER: _ClassVar[int]
    first_name: str
    last_name: str
    type: str
    app_type: str
    app_id: str
    name: str
    email: str
    admin: bool
    idp: str
    status: str
    expire_at: _timestamp_pb2.Timestamp
    def __init__(self, first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., type: _Optional[str] = ..., app_type: _Optional[str] = ..., app_id: _Optional[str] = ..., name: _Optional[str] = ..., email: _Optional[str] = ..., admin: bool = ..., idp: _Optional[str] = ..., status: _Optional[str] = ..., expire_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreateUserResponse(_message.Message):
    __slots__ = ["user", "tenant_id"]
    USER_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    user: _user_pb2.User
    tenant_id: str
    def __init__(self, user: _Optional[_Union[_user_pb2.User, _Mapping]] = ..., tenant_id: _Optional[str] = ...) -> None: ...

class CreateUserV2Request(_message.Message):
    __slots__ = ["first_name", "last_name", "type", "app_type", "app_id", "name", "email", "admin", "idp", "status", "expire_at"]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    APP_TYPE_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ADMIN_FIELD_NUMBER: _ClassVar[int]
    IDP_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_AT_FIELD_NUMBER: _ClassVar[int]
    first_name: str
    last_name: str
    type: str
    app_type: str
    app_id: str
    name: str
    email: str
    admin: bool
    idp: str
    status: str
    expire_at: _timestamp_pb2.Timestamp
    def __init__(self, first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., type: _Optional[str] = ..., app_type: _Optional[str] = ..., app_id: _Optional[str] = ..., name: _Optional[str] = ..., email: _Optional[str] = ..., admin: bool = ..., idp: _Optional[str] = ..., status: _Optional[str] = ..., expire_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreateUserV2Response(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetUserByIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetUserByIdResponse(_message.Message):
    __slots__ = ["user"]
    USER_FIELD_NUMBER: _ClassVar[int]
    user: _user_pb2.User
    def __init__(self, user: _Optional[_Union[_user_pb2.User, _Mapping]] = ...) -> None: ...

class DeleteUserRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteUserResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UpdateUserRequest(_message.Message):
    __slots__ = ["id", "name", "first_name", "last_name", "email"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    first_name: str
    last_name: str
    email: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class UpdateUserResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetMachineUserAuthTokenRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetMachineUserAuthTokenResponse(_message.Message):
    __slots__ = ["token", "username"]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    token: str
    username: str
    def __init__(self, token: _Optional[str] = ..., username: _Optional[str] = ...) -> None: ...

class RefreshMachineUserAuthTokenRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class RefreshMachineUserAuthTokenResponse(_message.Message):
    __slots__ = ["token", "username"]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    token: str
    username: str
    def __init__(self, token: _Optional[str] = ..., username: _Optional[str] = ...) -> None: ...

class GetUserExternalIdsRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetUserExternalIdsResponse(_message.Message):
    __slots__ = ["external_ids"]
    EXTERNAL_IDS_FIELD_NUMBER: _ClassVar[int]
    external_ids: _containers.RepeatedCompositeFieldContainer[_external_id_pb2.ExternalId]
    def __init__(self, external_ids: _Optional[_Iterable[_Union[_external_id_pb2.ExternalId, _Mapping]]] = ...) -> None: ...

class MapUserToExternalIdRequest(_message.Message):
    __slots__ = ["user_id", "external_id", "description", "app_id"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    external_id: str
    description: str
    app_id: str
    def __init__(self, user_id: _Optional[str] = ..., external_id: _Optional[str] = ..., description: _Optional[str] = ..., app_id: _Optional[str] = ...) -> None: ...

class MapUserToExternalIdResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteExternalIdMappingRequest(_message.Message):
    __slots__ = ["mapping_id"]
    MAPPING_ID_FIELD_NUMBER: _ClassVar[int]
    mapping_id: str
    def __init__(self, mapping_id: _Optional[str] = ...) -> None: ...

class DeleteExternalIdMappingResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
