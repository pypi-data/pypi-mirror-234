from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    CONNECTION_TYPE_UNSPECIFIED: _ClassVar[ConnectionType]
    CONNECTION_TYPE_ADFS_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_ADP_OIDC: _ClassVar[ConnectionType]
    CONNECTION_TYPE_AUTH0_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_AZURE_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_CAS_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_CLOUDFLARE_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_CLASS_LINK_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_CYBERARK_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_DUO_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_GENERIC_OIDC: _ClassVar[ConnectionType]
    CONNECTION_TYPE_GENERIC_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_GOOGLE_OAUTH: _ClassVar[ConnectionType]
    CONNECTION_TYPE_GOOGLE_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_JUMP_CLOUD_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_MAGIC_LINK: _ClassVar[ConnectionType]
    CONNECTION_TYPE_MICROSOFT_OAUTH: _ClassVar[ConnectionType]
    CONNECTION_TYPE_MINIORANGE_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_NETIQ_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_OKTA_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_ONELOGIN_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_ORACLE_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_PING_FEDERATE_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_PING_ONE_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_RIPPLING_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_SALESFORCE_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_SHIBBOLETH_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_SIMPLE_SAML_PHP_SAML: _ClassVar[ConnectionType]
    CONNECTION_TYPE_VMWARE_SAML: _ClassVar[ConnectionType]

class ConnectionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    CONNECTION_STATUS_UNSPECIFIED: _ClassVar[ConnectionStatus]
    CONNECTION_STATUS_LINKED: _ClassVar[ConnectionStatus]
    CONNECTION_STATUS_UNLINKED: _ClassVar[ConnectionStatus]

class ConnectionState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    CONNECTION_STATE_UNSPECIFIED: _ClassVar[ConnectionState]
    CONNECTION_STATE_DRAFT: _ClassVar[ConnectionState]
    CONNECTION_STATE_ACTIVE: _ClassVar[ConnectionState]
    CONNECTION_STATE_INACTIVE: _ClassVar[ConnectionState]
CONNECTION_TYPE_UNSPECIFIED: ConnectionType
CONNECTION_TYPE_ADFS_SAML: ConnectionType
CONNECTION_TYPE_ADP_OIDC: ConnectionType
CONNECTION_TYPE_AUTH0_SAML: ConnectionType
CONNECTION_TYPE_AZURE_SAML: ConnectionType
CONNECTION_TYPE_CAS_SAML: ConnectionType
CONNECTION_TYPE_CLOUDFLARE_SAML: ConnectionType
CONNECTION_TYPE_CLASS_LINK_SAML: ConnectionType
CONNECTION_TYPE_CYBERARK_SAML: ConnectionType
CONNECTION_TYPE_DUO_SAML: ConnectionType
CONNECTION_TYPE_GENERIC_OIDC: ConnectionType
CONNECTION_TYPE_GENERIC_SAML: ConnectionType
CONNECTION_TYPE_GOOGLE_OAUTH: ConnectionType
CONNECTION_TYPE_GOOGLE_SAML: ConnectionType
CONNECTION_TYPE_JUMP_CLOUD_SAML: ConnectionType
CONNECTION_TYPE_MAGIC_LINK: ConnectionType
CONNECTION_TYPE_MICROSOFT_OAUTH: ConnectionType
CONNECTION_TYPE_MINIORANGE_SAML: ConnectionType
CONNECTION_TYPE_NETIQ_SAML: ConnectionType
CONNECTION_TYPE_OKTA_SAML: ConnectionType
CONNECTION_TYPE_ONELOGIN_SAML: ConnectionType
CONNECTION_TYPE_ORACLE_SAML: ConnectionType
CONNECTION_TYPE_PING_FEDERATE_SAML: ConnectionType
CONNECTION_TYPE_PING_ONE_SAML: ConnectionType
CONNECTION_TYPE_RIPPLING_SAML: ConnectionType
CONNECTION_TYPE_SALESFORCE_SAML: ConnectionType
CONNECTION_TYPE_SHIBBOLETH_SAML: ConnectionType
CONNECTION_TYPE_SIMPLE_SAML_PHP_SAML: ConnectionType
CONNECTION_TYPE_VMWARE_SAML: ConnectionType
CONNECTION_STATUS_UNSPECIFIED: ConnectionStatus
CONNECTION_STATUS_LINKED: ConnectionStatus
CONNECTION_STATUS_UNLINKED: ConnectionStatus
CONNECTION_STATE_UNSPECIFIED: ConnectionState
CONNECTION_STATE_DRAFT: ConnectionState
CONNECTION_STATE_ACTIVE: ConnectionState
CONNECTION_STATE_INACTIVE: ConnectionState

class Connection(_message.Message):
    __slots__ = ["id", "status", "state", "name", "connection_type", "organization_id", "domains", "created_at", "updated_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    DOMAINS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: ConnectionStatus
    state: ConnectionState
    name: str
    connection_type: ConnectionType
    organization_id: str
    domains: _containers.RepeatedCompositeFieldContainer[ConnectionDomain]
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., status: _Optional[_Union[ConnectionStatus, str]] = ..., state: _Optional[_Union[ConnectionState, str]] = ..., name: _Optional[str] = ..., connection_type: _Optional[_Union[ConnectionType, str]] = ..., organization_id: _Optional[str] = ..., domains: _Optional[_Iterable[_Union[ConnectionDomain, _Mapping]]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class ConnectionDomain(_message.Message):
    __slots__ = ["id", "domain"]
    ID_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    id: str
    domain: str
    def __init__(self, id: _Optional[str] = ..., domain: _Optional[str] = ...) -> None: ...
