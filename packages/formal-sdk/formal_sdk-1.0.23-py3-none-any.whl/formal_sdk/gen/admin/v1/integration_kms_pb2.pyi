from .types.v1 import key_pb2 as _key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateKeyRegistrationRequest(_message.Message):
    __slots__ = ["cloud_region", "key_id", "managed_by", "key_type", "key_name", "cloud_account_id"]
    CLOUD_REGION_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    MANAGED_BY_FIELD_NUMBER: _ClassVar[int]
    KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
    KEY_NAME_FIELD_NUMBER: _ClassVar[int]
    CLOUD_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    cloud_region: str
    key_id: str
    managed_by: str
    key_type: str
    key_name: str
    cloud_account_id: str
    def __init__(self, cloud_region: _Optional[str] = ..., key_id: _Optional[str] = ..., managed_by: _Optional[str] = ..., key_type: _Optional[str] = ..., key_name: _Optional[str] = ..., cloud_account_id: _Optional[str] = ...) -> None: ...

class CreateKeyRegistrationResponse(_message.Message):
    __slots__ = ["key"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: _key_pb2.Key
    def __init__(self, key: _Optional[_Union[_key_pb2.Key, _Mapping]] = ...) -> None: ...

class GetKeysRequest(_message.Message):
    __slots__ = ["filter_by_status"]
    FILTER_BY_STATUS_FIELD_NUMBER: _ClassVar[int]
    filter_by_status: str
    def __init__(self, filter_by_status: _Optional[str] = ...) -> None: ...

class GetKeysResponse(_message.Message):
    __slots__ = ["keys"]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedCompositeFieldContainer[_key_pb2.Key]
    def __init__(self, keys: _Optional[_Iterable[_Union[_key_pb2.Key, _Mapping]]] = ...) -> None: ...

class GetKeyRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetKeyResponse(_message.Message):
    __slots__ = ["key"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: _key_pb2.Key
    def __init__(self, key: _Optional[_Union[_key_pb2.Key, _Mapping]] = ...) -> None: ...

class DeactivateFieldEncryptionKeyRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeactivateFieldEncryptionKeyResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
