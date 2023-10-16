from .types.v1 import sidecar_pb2 as _sidecar_pb2
from .types.v1 import sidecar_link_pb2 as _sidecar_link_pb2
from ...validate.v1 import validate_pb2 as _validate_pb2
from .types.v1 import list_metadata_pb2 as _list_metadata_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListSidecarsRequest(_message.Message):
    __slots__ = ["limit", "cursor", "order"]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    order: str
    def __init__(self, limit: _Optional[int] = ..., cursor: _Optional[str] = ..., order: _Optional[str] = ...) -> None: ...

class ListSidecarsResponse(_message.Message):
    __slots__ = ["sidecars", "list_metadata"]
    SIDECARS_FIELD_NUMBER: _ClassVar[int]
    LIST_METADATA_FIELD_NUMBER: _ClassVar[int]
    sidecars: _containers.RepeatedCompositeFieldContainer[_sidecar_pb2.Sidecar]
    list_metadata: _list_metadata_pb2.ListMetadata
    def __init__(self, sidecars: _Optional[_Iterable[_Union[_sidecar_pb2.Sidecar, _Mapping]]] = ..., list_metadata: _Optional[_Union[_list_metadata_pb2.ListMetadata, _Mapping]] = ...) -> None: ...

class GetSidecarVersionsRequest(_message.Message):
    __slots__ = ["technology"]
    TECHNOLOGY_FIELD_NUMBER: _ClassVar[int]
    technology: str
    def __init__(self, technology: _Optional[str] = ...) -> None: ...

class GetSidecarVersionsResponse(_message.Message):
    __slots__ = ["versions"]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    versions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, versions: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateSidecarRequest(_message.Message):
    __slots__ = ["name", "technology", "deployment_type", "dataplane_id", "datastore_id", "fail_open", "global_kms_decrypt", "formal_hostname", "version", "network_type"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TECHNOLOGY_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATAPLANE_ID_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    FAIL_OPEN_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_KMS_DECRYPT_FIELD_NUMBER: _ClassVar[int]
    FORMAL_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    NETWORK_TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    technology: str
    deployment_type: str
    dataplane_id: str
    datastore_id: str
    fail_open: bool
    global_kms_decrypt: bool
    formal_hostname: str
    version: str
    network_type: str
    def __init__(self, name: _Optional[str] = ..., technology: _Optional[str] = ..., deployment_type: _Optional[str] = ..., dataplane_id: _Optional[str] = ..., datastore_id: _Optional[str] = ..., fail_open: bool = ..., global_kms_decrypt: bool = ..., formal_hostname: _Optional[str] = ..., version: _Optional[str] = ..., network_type: _Optional[str] = ...) -> None: ...

class CreateSidecarResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetSidecarByIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetSidecarByIdResponse(_message.Message):
    __slots__ = ["sidecar"]
    SIDECAR_FIELD_NUMBER: _ClassVar[int]
    sidecar: _sidecar_pb2.Sidecar
    def __init__(self, sidecar: _Optional[_Union[_sidecar_pb2.Sidecar, _Mapping]] = ...) -> None: ...

class GetSidecarTlsCertificateByIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetSidecarTlsCertificateByIdResponse(_message.Message):
    __slots__ = ["secret"]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    secret: str
    def __init__(self, secret: _Optional[str] = ...) -> None: ...

class UpdateSidecarNameRequest(_message.Message):
    __slots__ = ["id", "name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class UpdateSidecarNameResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UpdateSidecarVersionRequest(_message.Message):
    __slots__ = ["id", "version"]
    ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    id: str
    version: str
    def __init__(self, id: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class UpdateSidecarVersionResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UpdateSidecarFormalHostnameRequest(_message.Message):
    __slots__ = ["id", "hostname"]
    ID_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    hostname: str
    def __init__(self, id: _Optional[str] = ..., hostname: _Optional[str] = ...) -> None: ...

class UpdateSidecarFormalHostnameResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UpdateSidecarKmsDecryptPolicyRequest(_message.Message):
    __slots__ = ["id", "enabled"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    id: str
    enabled: bool
    def __init__(self, id: _Optional[str] = ..., enabled: bool = ...) -> None: ...

class UpdateSidecarKmsDecryptPolicyResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteSidecarRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteSidecarResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CreateSidecarDatastoreLinkRequest(_message.Message):
    __slots__ = ["datastore_id", "sidecar_id", "port"]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    SIDECAR_ID_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    datastore_id: str
    sidecar_id: str
    port: int
    def __init__(self, datastore_id: _Optional[str] = ..., sidecar_id: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class CreateSidecarDatastoreLinkResponse(_message.Message):
    __slots__ = ["link_id"]
    LINK_ID_FIELD_NUMBER: _ClassVar[int]
    link_id: str
    def __init__(self, link_id: _Optional[str] = ...) -> None: ...

class DeleteSidecarDatastoreLinkRequest(_message.Message):
    __slots__ = ["link_id"]
    LINK_ID_FIELD_NUMBER: _ClassVar[int]
    link_id: str
    def __init__(self, link_id: _Optional[str] = ...) -> None: ...

class DeleteSidecarDatastoreLinkResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetLinkByIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetLinkByIdResponse(_message.Message):
    __slots__ = ["link"]
    LINK_FIELD_NUMBER: _ClassVar[int]
    link: _sidecar_link_pb2.SidecarLink
    def __init__(self, link: _Optional[_Union[_sidecar_link_pb2.SidecarLink, _Mapping]] = ...) -> None: ...

class GetLinksBySidecarIdRequest(_message.Message):
    __slots__ = ["sidecar_id"]
    SIDECAR_ID_FIELD_NUMBER: _ClassVar[int]
    sidecar_id: str
    def __init__(self, sidecar_id: _Optional[str] = ...) -> None: ...

class GetLinksBySidecarIdResponse(_message.Message):
    __slots__ = ["links"]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    links: _containers.RepeatedCompositeFieldContainer[_sidecar_link_pb2.SidecarLink]
    def __init__(self, links: _Optional[_Iterable[_Union[_sidecar_link_pb2.SidecarLink, _Mapping]]] = ...) -> None: ...

class GetLinksByDatastoreIdRequest(_message.Message):
    __slots__ = ["datastore_id"]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    datastore_id: str
    def __init__(self, datastore_id: _Optional[str] = ...) -> None: ...

class GetLinksByDatastoreIdResponse(_message.Message):
    __slots__ = ["links"]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    links: _containers.RepeatedCompositeFieldContainer[_sidecar_link_pb2.SidecarLink]
    def __init__(self, links: _Optional[_Iterable[_Union[_sidecar_link_pb2.SidecarLink, _Mapping]]] = ...) -> None: ...
