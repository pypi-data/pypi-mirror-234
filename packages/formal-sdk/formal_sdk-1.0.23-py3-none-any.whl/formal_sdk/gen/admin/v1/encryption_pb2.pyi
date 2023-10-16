from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateOrUpdateDefaultFieldEncryptionPolicyRequest(_message.Message):
    __slots__ = ["kms_key_id", "encryption_alg", "data_key_storage"]
    KMS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTION_ALG_FIELD_NUMBER: _ClassVar[int]
    DATA_KEY_STORAGE_FIELD_NUMBER: _ClassVar[int]
    kms_key_id: str
    encryption_alg: str
    data_key_storage: str
    def __init__(self, kms_key_id: _Optional[str] = ..., encryption_alg: _Optional[str] = ..., data_key_storage: _Optional[str] = ...) -> None: ...

class CreateOrUpdateDefaultFieldEncryptionPolicyResponse(_message.Message):
    __slots__ = ["default_field_encryption_policy"]
    DEFAULT_FIELD_ENCRYPTION_POLICY_FIELD_NUMBER: _ClassVar[int]
    default_field_encryption_policy: DefaultFieldEncryptionPolicy
    def __init__(self, default_field_encryption_policy: _Optional[_Union[DefaultFieldEncryptionPolicy, _Mapping]] = ...) -> None: ...

class GetDefaultFieldEncryptionPolicyRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetDefaultFieldEncryptionPolicyResponse(_message.Message):
    __slots__ = ["default_field_encryption_policy"]
    DEFAULT_FIELD_ENCRYPTION_POLICY_FIELD_NUMBER: _ClassVar[int]
    default_field_encryption_policy: DefaultFieldEncryptionPolicy
    def __init__(self, default_field_encryption_policy: _Optional[_Union[DefaultFieldEncryptionPolicy, _Mapping]] = ...) -> None: ...

class DefaultFieldEncryptionPolicy(_message.Message):
    __slots__ = ["kms_key_id", "encryption_alg", "data_key_storage", "updated_at"]
    KMS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTION_ALG_FIELD_NUMBER: _ClassVar[int]
    DATA_KEY_STORAGE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    kms_key_id: str
    encryption_alg: str
    data_key_storage: str
    updated_at: int
    def __init__(self, kms_key_id: _Optional[str] = ..., encryption_alg: _Optional[str] = ..., data_key_storage: _Optional[str] = ..., updated_at: _Optional[int] = ...) -> None: ...

class CreateFieldEncryptionRequest(_message.Message):
    __slots__ = ["path", "key_storage", "key_id", "alg", "datastore_id"]
    PATH_FIELD_NUMBER: _ClassVar[int]
    KEY_STORAGE_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    ALG_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    path: str
    key_storage: str
    key_id: str
    alg: str
    datastore_id: str
    def __init__(self, path: _Optional[str] = ..., key_storage: _Optional[str] = ..., key_id: _Optional[str] = ..., alg: _Optional[str] = ..., datastore_id: _Optional[str] = ...) -> None: ...

class CreateFieldEncryptionResponse(_message.Message):
    __slots__ = ["field_encryption"]
    FIELD_ENCRYPTION_FIELD_NUMBER: _ClassVar[int]
    field_encryption: FieldEncryption
    def __init__(self, field_encryption: _Optional[_Union[FieldEncryption, _Mapping]] = ...) -> None: ...

class GetFieldEncryptionsByDatastoreRequest(_message.Message):
    __slots__ = ["datastore_id"]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    datastore_id: str
    def __init__(self, datastore_id: _Optional[str] = ...) -> None: ...

class GetFieldEncryptionsByDatastoreResponse(_message.Message):
    __slots__ = ["field_encryptions"]
    FIELD_ENCRYPTIONS_FIELD_NUMBER: _ClassVar[int]
    field_encryptions: _containers.RepeatedCompositeFieldContainer[FieldEncryption]
    def __init__(self, field_encryptions: _Optional[_Iterable[_Union[FieldEncryption, _Mapping]]] = ...) -> None: ...

class DeleteFieldEncryptionRequest(_message.Message):
    __slots__ = ["datastore_id", "field_encryption_id"]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    FIELD_ENCRYPTION_ID_FIELD_NUMBER: _ClassVar[int]
    datastore_id: str
    field_encryption_id: str
    def __init__(self, datastore_id: _Optional[str] = ..., field_encryption_id: _Optional[str] = ...) -> None: ...

class DeleteFieldEncryptionResponse(_message.Message):
    __slots__ = ["datastore_id"]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    datastore_id: str
    def __init__(self, datastore_id: _Optional[str] = ...) -> None: ...

class FieldEncryption(_message.Message):
    __slots__ = ["datastore_id", "name", "path", "key_storage", "key_id", "key_region", "alg"]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    KEY_STORAGE_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_REGION_FIELD_NUMBER: _ClassVar[int]
    ALG_FIELD_NUMBER: _ClassVar[int]
    datastore_id: str
    name: str
    path: str
    key_storage: str
    key_id: str
    key_region: str
    alg: str
    def __init__(self, datastore_id: _Optional[str] = ..., name: _Optional[str] = ..., path: _Optional[str] = ..., key_storage: _Optional[str] = ..., key_id: _Optional[str] = ..., key_region: _Optional[str] = ..., alg: _Optional[str] = ...) -> None: ...
