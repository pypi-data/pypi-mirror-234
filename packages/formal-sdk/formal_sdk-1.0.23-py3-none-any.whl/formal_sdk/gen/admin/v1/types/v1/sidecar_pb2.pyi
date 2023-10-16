from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeploymentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    DEPLOYMENT_TYPE_UNSPECIFIED: _ClassVar[DeploymentType]
    DEPLOYMENT_TYPE_ONPREM: _ClassVar[DeploymentType]
    DEPLOYMENT_TYPE_MANAGED: _ClassVar[DeploymentType]

class NetworkType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    NETWORK_TYPE_UNSPECIFIED: _ClassVar[NetworkType]
    NETWORK_TYPE_INTERNET_FACING: _ClassVar[NetworkType]
    NETWORK_TYPE_INTERNAL: _ClassVar[NetworkType]
    NETWORK_TYPE_INTERNET_AND_INTERNAL: _ClassVar[NetworkType]

class CloudProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    CLOUD_PROVIDER_UNSPECIFIED: _ClassVar[CloudProvider]
    CLOUD_PROVIDER_AWS: _ClassVar[CloudProvider]
    CLOUD_PROVIDER_AZURE: _ClassVar[CloudProvider]
    CLOUD_PROVIDER_GCP: _ClassVar[CloudProvider]
DEPLOYMENT_TYPE_UNSPECIFIED: DeploymentType
DEPLOYMENT_TYPE_ONPREM: DeploymentType
DEPLOYMENT_TYPE_MANAGED: DeploymentType
NETWORK_TYPE_UNSPECIFIED: NetworkType
NETWORK_TYPE_INTERNET_FACING: NetworkType
NETWORK_TYPE_INTERNAL: NetworkType
NETWORK_TYPE_INTERNET_AND_INTERNAL: NetworkType
CLOUD_PROVIDER_UNSPECIFIED: CloudProvider
CLOUD_PROVIDER_AWS: CloudProvider
CLOUD_PROVIDER_AZURE: CloudProvider
CLOUD_PROVIDER_GCP: CloudProvider

class Sidecar(_message.Message):
    __slots__ = ["id", "name", "cloud_account_id", "cloud_provider", "cloud_region", "technology", "deployment_type", "network_type", "dataplane_id", "datastore_id", "deployed", "version", "formal_hostname", "server_connection_status", "proxy_status", "fail_open", "global_kms_decrypt", "ssh_rsa_key", "server_error_message", "created_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CLOUD_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    CLOUD_REGION_FIELD_NUMBER: _ClassVar[int]
    TECHNOLOGY_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    NETWORK_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATAPLANE_ID_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYED_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    FORMAL_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    SERVER_CONNECTION_STATUS_FIELD_NUMBER: _ClassVar[int]
    PROXY_STATUS_FIELD_NUMBER: _ClassVar[int]
    FAIL_OPEN_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_KMS_DECRYPT_FIELD_NUMBER: _ClassVar[int]
    SSH_RSA_KEY_FIELD_NUMBER: _ClassVar[int]
    SERVER_ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    cloud_account_id: str
    cloud_provider: CloudProvider
    cloud_region: str
    technology: str
    deployment_type: str
    network_type: str
    dataplane_id: str
    datastore_id: str
    deployed: bool
    version: str
    formal_hostname: str
    server_connection_status: str
    proxy_status: str
    fail_open: bool
    global_kms_decrypt: bool
    ssh_rsa_key: bytes
    server_error_message: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., cloud_account_id: _Optional[str] = ..., cloud_provider: _Optional[_Union[CloudProvider, str]] = ..., cloud_region: _Optional[str] = ..., technology: _Optional[str] = ..., deployment_type: _Optional[str] = ..., network_type: _Optional[str] = ..., dataplane_id: _Optional[str] = ..., datastore_id: _Optional[str] = ..., deployed: bool = ..., version: _Optional[str] = ..., formal_hostname: _Optional[str] = ..., server_connection_status: _Optional[str] = ..., proxy_status: _Optional[str] = ..., fail_open: bool = ..., global_kms_decrypt: bool = ..., ssh_rsa_key: _Optional[bytes] = ..., server_error_message: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
