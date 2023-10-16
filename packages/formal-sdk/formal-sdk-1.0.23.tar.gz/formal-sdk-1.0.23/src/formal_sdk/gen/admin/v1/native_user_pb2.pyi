from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateNativeUserRequest(_message.Message):
    __slots__ = ["data_store_id", "native_user_id", "native_user_secret", "use_as_default"]
    DATA_STORE_ID_FIELD_NUMBER: _ClassVar[int]
    NATIVE_USER_ID_FIELD_NUMBER: _ClassVar[int]
    NATIVE_USER_SECRET_FIELD_NUMBER: _ClassVar[int]
    USE_AS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    data_store_id: str
    native_user_id: str
    native_user_secret: str
    use_as_default: bool
    def __init__(self, data_store_id: _Optional[str] = ..., native_user_id: _Optional[str] = ..., native_user_secret: _Optional[str] = ..., use_as_default: bool = ...) -> None: ...

class CreateNativeUserResponse(_message.Message):
    __slots__ = ["native_user"]
    NATIVE_USER_FIELD_NUMBER: _ClassVar[int]
    native_user: NativeUser
    def __init__(self, native_user: _Optional[_Union[NativeUser, _Mapping]] = ...) -> None: ...

class GetNativeUsersRequest(_message.Message):
    __slots__ = ["data_store_id"]
    DATA_STORE_ID_FIELD_NUMBER: _ClassVar[int]
    data_store_id: str
    def __init__(self, data_store_id: _Optional[str] = ...) -> None: ...

class GetNativeUsersResponse(_message.Message):
    __slots__ = ["native_users"]
    class NativeUsersEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: NativeUser
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[NativeUser, _Mapping]] = ...) -> None: ...
    NATIVE_USERS_FIELD_NUMBER: _ClassVar[int]
    native_users: _containers.MessageMap[str, NativeUser]
    def __init__(self, native_users: _Optional[_Mapping[str, NativeUser]] = ...) -> None: ...

class GetNativeUserRequest(_message.Message):
    __slots__ = ["data_store_id", "native_user_id"]
    DATA_STORE_ID_FIELD_NUMBER: _ClassVar[int]
    NATIVE_USER_ID_FIELD_NUMBER: _ClassVar[int]
    data_store_id: str
    native_user_id: str
    def __init__(self, data_store_id: _Optional[str] = ..., native_user_id: _Optional[str] = ...) -> None: ...

class GetNativeUserResponse(_message.Message):
    __slots__ = ["native_user"]
    NATIVE_USER_FIELD_NUMBER: _ClassVar[int]
    native_user: NativeUser
    def __init__(self, native_user: _Optional[_Union[NativeUser, _Mapping]] = ...) -> None: ...

class NativeUser(_message.Message):
    __slots__ = ["datastore_id", "native_user_id", "native_user_secret", "use_as_default", "created_at", "users", "groups"]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    NATIVE_USER_ID_FIELD_NUMBER: _ClassVar[int]
    NATIVE_USER_SECRET_FIELD_NUMBER: _ClassVar[int]
    USE_AS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    datastore_id: str
    native_user_id: str
    native_user_secret: str
    use_as_default: bool
    created_at: int
    users: _containers.RepeatedScalarFieldContainer[str]
    groups: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, datastore_id: _Optional[str] = ..., native_user_id: _Optional[str] = ..., native_user_secret: _Optional[str] = ..., use_as_default: bool = ..., created_at: _Optional[int] = ..., users: _Optional[_Iterable[str]] = ..., groups: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteNativeUserRequest(_message.Message):
    __slots__ = ["data_store_id", "native_user_id"]
    DATA_STORE_ID_FIELD_NUMBER: _ClassVar[int]
    NATIVE_USER_ID_FIELD_NUMBER: _ClassVar[int]
    data_store_id: str
    native_user_id: str
    def __init__(self, data_store_id: _Optional[str] = ..., native_user_id: _Optional[str] = ...) -> None: ...

class DeleteNativeUserResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UpdateNativeUserSecretRequest(_message.Message):
    __slots__ = ["data_store_id", "native_user_id", "native_user_secret"]
    DATA_STORE_ID_FIELD_NUMBER: _ClassVar[int]
    NATIVE_USER_ID_FIELD_NUMBER: _ClassVar[int]
    NATIVE_USER_SECRET_FIELD_NUMBER: _ClassVar[int]
    data_store_id: str
    native_user_id: str
    native_user_secret: str
    def __init__(self, data_store_id: _Optional[str] = ..., native_user_id: _Optional[str] = ..., native_user_secret: _Optional[str] = ...) -> None: ...

class UpdateNativeUserSecretResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SetNativeUserAsDefaultRequest(_message.Message):
    __slots__ = ["data_store_id", "native_user_id"]
    DATA_STORE_ID_FIELD_NUMBER: _ClassVar[int]
    NATIVE_USER_ID_FIELD_NUMBER: _ClassVar[int]
    data_store_id: str
    native_user_id: str
    def __init__(self, data_store_id: _Optional[str] = ..., native_user_id: _Optional[str] = ...) -> None: ...

class SetNativeUserAsDefaultResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CreateNativeUserIdentityLinkRequest(_message.Message):
    __slots__ = ["data_store_id", "native_user_id", "identity_id", "formal_identity_type"]
    DATA_STORE_ID_FIELD_NUMBER: _ClassVar[int]
    NATIVE_USER_ID_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    FORMAL_IDENTITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    data_store_id: str
    native_user_id: str
    identity_id: str
    formal_identity_type: str
    def __init__(self, data_store_id: _Optional[str] = ..., native_user_id: _Optional[str] = ..., identity_id: _Optional[str] = ..., formal_identity_type: _Optional[str] = ...) -> None: ...

class CreateNativeUserIdentityLinkResponse(_message.Message):
    __slots__ = ["link"]
    LINK_FIELD_NUMBER: _ClassVar[int]
    link: NativeUserLink
    def __init__(self, link: _Optional[_Union[NativeUserLink, _Mapping]] = ...) -> None: ...

class GetNativeUserIdentityLinkRequest(_message.Message):
    __slots__ = ["data_store_id", "identity_id"]
    DATA_STORE_ID_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    data_store_id: str
    identity_id: str
    def __init__(self, data_store_id: _Optional[str] = ..., identity_id: _Optional[str] = ...) -> None: ...

class CreateNativeUserIdentityLinkV2Request(_message.Message):
    __slots__ = ["data_store_id", "native_user_id", "identity_id", "formal_identity_type"]
    DATA_STORE_ID_FIELD_NUMBER: _ClassVar[int]
    NATIVE_USER_ID_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    FORMAL_IDENTITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    data_store_id: str
    native_user_id: str
    identity_id: str
    formal_identity_type: str
    def __init__(self, data_store_id: _Optional[str] = ..., native_user_id: _Optional[str] = ..., identity_id: _Optional[str] = ..., formal_identity_type: _Optional[str] = ...) -> None: ...

class CreateNativeUserIdentityLinkV2Response(_message.Message):
    __slots__ = ["link"]
    LINK_FIELD_NUMBER: _ClassVar[int]
    link: NativeUserLink
    def __init__(self, link: _Optional[_Union[NativeUserLink, _Mapping]] = ...) -> None: ...

class GetNativeUserIdentityLinkResponse(_message.Message):
    __slots__ = ["link"]
    LINK_FIELD_NUMBER: _ClassVar[int]
    link: NativeUserLink
    def __init__(self, link: _Optional[_Union[NativeUserLink, _Mapping]] = ...) -> None: ...

class DeleteNativeUserIdentityLinkRequest(_message.Message):
    __slots__ = ["data_store_id", "identity_id"]
    DATA_STORE_ID_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    data_store_id: str
    identity_id: str
    def __init__(self, data_store_id: _Optional[str] = ..., identity_id: _Optional[str] = ...) -> None: ...

class DeleteNativeUserIdentityLinkResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class NativeUserLink(_message.Message):
    __slots__ = ["data_store_id", "formal_identity_id", "formal_identity_type", "native_user_id"]
    DATA_STORE_ID_FIELD_NUMBER: _ClassVar[int]
    FORMAL_IDENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    FORMAL_IDENTITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    NATIVE_USER_ID_FIELD_NUMBER: _ClassVar[int]
    data_store_id: str
    formal_identity_id: str
    formal_identity_type: str
    native_user_id: str
    def __init__(self, data_store_id: _Optional[str] = ..., formal_identity_id: _Optional[str] = ..., formal_identity_type: _Optional[str] = ..., native_user_id: _Optional[str] = ...) -> None: ...
