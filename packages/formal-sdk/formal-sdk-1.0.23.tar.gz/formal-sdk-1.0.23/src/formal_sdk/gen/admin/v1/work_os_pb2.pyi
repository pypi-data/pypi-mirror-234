from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetDirectoryRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetDirectoryResponse(_message.Message):
    __slots__ = ["directory"]
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    directory: Directory
    def __init__(self, directory: _Optional[_Union[Directory, _Mapping]] = ...) -> None: ...

class Directory(_message.Message):
    __slots__ = ["id", "name", "idp_id", "directory_id", "created_at", "updated_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IDP_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    idp_id: str
    directory_id: str
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., idp_id: _Optional[str] = ..., directory_id: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class GetGroupsByDirectoryIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetGroupsByDirectoryIdResponse(_message.Message):
    __slots__ = ["groups"]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    groups: _containers.RepeatedCompositeFieldContainer[DirectorySyncGroup]
    def __init__(self, groups: _Optional[_Iterable[_Union[DirectorySyncGroup, _Mapping]]] = ...) -> None: ...

class GetUsersByDirectoryIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetUsersByDirectoryIdResponse(_message.Message):
    __slots__ = ["users"]
    USERS_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[WorkUser]
    def __init__(self, users: _Optional[_Iterable[_Union[WorkUser, _Mapping]]] = ...) -> None: ...

class GetWorkOsGroupByIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetWorkOsGroupByIdResponse(_message.Message):
    __slots__ = ["group"]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: DirectorySyncGroup
    def __init__(self, group: _Optional[_Union[DirectorySyncGroup, _Mapping]] = ...) -> None: ...

class DirectorySyncGroup(_message.Message):
    __slots__ = ["id", "name", "idp_id", "directory_id", "created_at", "updated_at", "mapped_formal_group_id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IDP_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    MAPPED_FORMAL_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    idp_id: str
    directory_id: str
    created_at: str
    updated_at: str
    mapped_formal_group_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., idp_id: _Optional[str] = ..., directory_id: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., mapped_formal_group_id: _Optional[str] = ...) -> None: ...

class UserEmail(_message.Message):
    __slots__ = ["primary", "value", "type"]
    PRIMARY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    primary: bool
    value: str
    type: str
    def __init__(self, primary: bool = ..., value: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class UserGroup(_message.Message):
    __slots__ = ["object", "id", "name"]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    object: str
    id: str
    name: str
    def __init__(self, object: _Optional[str] = ..., id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class WorkUser(_message.Message):
    __slots__ = ["id", "idp_id", "directory_id", "username", "emails", "first_name", "last_name", "job_title", "state", "created_at", "updated_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    IDP_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EMAILS_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    JOB_TITLE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    idp_id: str
    directory_id: str
    username: str
    emails: _containers.RepeatedCompositeFieldContainer[UserEmail]
    first_name: str
    last_name: str
    job_title: str
    state: str
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., idp_id: _Optional[str] = ..., directory_id: _Optional[str] = ..., username: _Optional[str] = ..., emails: _Optional[_Iterable[_Union[UserEmail, _Mapping]]] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., job_title: _Optional[str] = ..., state: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class Users(_message.Message):
    __slots__ = ["users"]
    USERS_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[WorkUser]
    def __init__(self, users: _Optional[_Iterable[_Union[WorkUser, _Mapping]]] = ...) -> None: ...

class Group(_message.Message):
    __slots__ = ["id", "name", "description", "active", "status", "created_at", "user_ids", "dsync_group_id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    DSYNC_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    active: bool
    status: str
    created_at: _timestamp_pb2.Timestamp
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    dsync_group_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., active: bool = ..., status: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., user_ids: _Optional[_Iterable[str]] = ..., dsync_group_id: _Optional[str] = ...) -> None: ...

class GroupPair(_message.Message):
    __slots__ = ["f_group", "d_group"]
    F_GROUP_FIELD_NUMBER: _ClassVar[int]
    D_GROUP_FIELD_NUMBER: _ClassVar[int]
    f_group: Group
    d_group: DirectorySyncGroup
    def __init__(self, f_group: _Optional[_Union[Group, _Mapping]] = ..., d_group: _Optional[_Union[DirectorySyncGroup, _Mapping]] = ...) -> None: ...

class GetDirectoryGroupsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetDirectoryGroupsResponse(_message.Message):
    __slots__ = ["directory_ids", "f_groups", "d_groups", "group_pairs", "d_group_users"]
    class DGroupUsersEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Users
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Users, _Mapping]] = ...) -> None: ...
    DIRECTORY_IDS_FIELD_NUMBER: _ClassVar[int]
    F_GROUPS_FIELD_NUMBER: _ClassVar[int]
    D_GROUPS_FIELD_NUMBER: _ClassVar[int]
    GROUP_PAIRS_FIELD_NUMBER: _ClassVar[int]
    D_GROUP_USERS_FIELD_NUMBER: _ClassVar[int]
    directory_ids: _containers.RepeatedScalarFieldContainer[str]
    f_groups: _containers.RepeatedCompositeFieldContainer[Group]
    d_groups: _containers.RepeatedCompositeFieldContainer[DirectorySyncGroup]
    group_pairs: _containers.RepeatedCompositeFieldContainer[GroupPair]
    d_group_users: _containers.MessageMap[str, Users]
    def __init__(self, directory_ids: _Optional[_Iterable[str]] = ..., f_groups: _Optional[_Iterable[_Union[Group, _Mapping]]] = ..., d_groups: _Optional[_Iterable[_Union[DirectorySyncGroup, _Mapping]]] = ..., group_pairs: _Optional[_Iterable[_Union[GroupPair, _Mapping]]] = ..., d_group_users: _Optional[_Mapping[str, Users]] = ...) -> None: ...

class UpdateDirectoryGroupSyncRequest(_message.Message):
    __slots__ = ["f_group_id", "d_group_id", "deselected_user_ids"]
    class DeselectedUserIdsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bool
        def __init__(self, key: _Optional[str] = ..., value: bool = ...) -> None: ...
    F_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    D_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    DESELECTED_USER_IDS_FIELD_NUMBER: _ClassVar[int]
    f_group_id: str
    d_group_id: str
    deselected_user_ids: _containers.ScalarMap[str, bool]
    def __init__(self, f_group_id: _Optional[str] = ..., d_group_id: _Optional[str] = ..., deselected_user_ids: _Optional[_Mapping[str, bool]] = ...) -> None: ...

class UpdateDirectoryGroupSyncResponse(_message.Message):
    __slots__ = ["f_group_id"]
    F_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    f_group_id: str
    def __init__(self, f_group_id: _Optional[str] = ...) -> None: ...

class GetDSyncPortalRequest(_message.Message):
    __slots__ = ["auth_token"]
    AUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    auth_token: str
    def __init__(self, auth_token: _Optional[str] = ...) -> None: ...

class GetDSyncPortalResponse(_message.Message):
    __slots__ = ["link"]
    LINK_FIELD_NUMBER: _ClassVar[int]
    link: str
    def __init__(self, link: _Optional[str] = ...) -> None: ...
