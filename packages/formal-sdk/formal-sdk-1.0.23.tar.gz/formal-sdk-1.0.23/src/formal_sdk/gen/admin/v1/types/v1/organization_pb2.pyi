from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Organization(_message.Message):
    __slots__ = ["id", "name", "allow_profiles_outside_organization", "domains", "created_at", "updated_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ALLOW_PROFILES_OUTSIDE_ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    DOMAINS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    allow_profiles_outside_organization: bool
    domains: _containers.RepeatedCompositeFieldContainer[OrganizationDomain]
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., allow_profiles_outside_organization: bool = ..., domains: _Optional[_Iterable[_Union[OrganizationDomain, _Mapping]]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class OrganizationDomain(_message.Message):
    __slots__ = ["id", "domain"]
    ID_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    id: str
    domain: str
    def __init__(self, id: _Optional[str] = ..., domain: _Optional[str] = ...) -> None: ...
