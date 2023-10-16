from .types.v1 import search_pb2 as _search_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchRequest(_message.Message):
    __slots__ = ["object_type", "query", "filter_by", "sort_by", "page", "limit"]
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    FILTER_BY_FIELD_NUMBER: _ClassVar[int]
    SORT_BY_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    object_type: str
    query: str
    filter_by: str
    sort_by: str
    page: int
    limit: int
    def __init__(self, object_type: _Optional[str] = ..., query: _Optional[str] = ..., filter_by: _Optional[str] = ..., sort_by: _Optional[str] = ..., page: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class SearchResponse(_message.Message):
    __slots__ = ["users", "groups", "policies", "datastores", "sidecars", "inventories", "found", "page", "out_of", "search_time_ms", "search_cutoff"]
    USERS_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    DATASTORES_FIELD_NUMBER: _ClassVar[int]
    SIDECARS_FIELD_NUMBER: _ClassVar[int]
    INVENTORIES_FIELD_NUMBER: _ClassVar[int]
    FOUND_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    OUT_OF_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    SEARCH_CUTOFF_FIELD_NUMBER: _ClassVar[int]
    users: WrappedSearchUser
    groups: WrappedSearchGroup
    policies: WrappedSearchPolicy
    datastores: WrappedSearchDatastore
    sidecars: WrappedSearchSidecar
    inventories: WrappedSearchInventory
    found: int
    page: int
    out_of: int
    search_time_ms: int
    search_cutoff: bool
    def __init__(self, users: _Optional[_Union[WrappedSearchUser, _Mapping]] = ..., groups: _Optional[_Union[WrappedSearchGroup, _Mapping]] = ..., policies: _Optional[_Union[WrappedSearchPolicy, _Mapping]] = ..., datastores: _Optional[_Union[WrappedSearchDatastore, _Mapping]] = ..., sidecars: _Optional[_Union[WrappedSearchSidecar, _Mapping]] = ..., inventories: _Optional[_Union[WrappedSearchInventory, _Mapping]] = ..., found: _Optional[int] = ..., page: _Optional[int] = ..., out_of: _Optional[int] = ..., search_time_ms: _Optional[int] = ..., search_cutoff: bool = ...) -> None: ...

class WrappedSearchUser(_message.Message):
    __slots__ = ["user"]
    USER_FIELD_NUMBER: _ClassVar[int]
    user: _containers.RepeatedCompositeFieldContainer[_search_pb2.SearchUser]
    def __init__(self, user: _Optional[_Iterable[_Union[_search_pb2.SearchUser, _Mapping]]] = ...) -> None: ...

class WrappedSearchGroup(_message.Message):
    __slots__ = ["group"]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: _containers.RepeatedCompositeFieldContainer[_search_pb2.SearchGroup]
    def __init__(self, group: _Optional[_Iterable[_Union[_search_pb2.SearchGroup, _Mapping]]] = ...) -> None: ...

class WrappedSearchPolicy(_message.Message):
    __slots__ = ["policy"]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: _containers.RepeatedCompositeFieldContainer[_search_pb2.SearchPolicy]
    def __init__(self, policy: _Optional[_Iterable[_Union[_search_pb2.SearchPolicy, _Mapping]]] = ...) -> None: ...

class WrappedSearchDatastore(_message.Message):
    __slots__ = ["datastore"]
    DATASTORE_FIELD_NUMBER: _ClassVar[int]
    datastore: _containers.RepeatedCompositeFieldContainer[_search_pb2.SearchDatastore]
    def __init__(self, datastore: _Optional[_Iterable[_Union[_search_pb2.SearchDatastore, _Mapping]]] = ...) -> None: ...

class WrappedSearchSidecar(_message.Message):
    __slots__ = ["sidecar"]
    SIDECAR_FIELD_NUMBER: _ClassVar[int]
    sidecar: _containers.RepeatedCompositeFieldContainer[_search_pb2.SearchSidecar]
    def __init__(self, sidecar: _Optional[_Iterable[_Union[_search_pb2.SearchSidecar, _Mapping]]] = ...) -> None: ...

class WrappedSearchInventory(_message.Message):
    __slots__ = ["inventory"]
    INVENTORY_FIELD_NUMBER: _ClassVar[int]
    inventory: _containers.RepeatedCompositeFieldContainer[_search_pb2.SearchInventory]
    def __init__(self, inventory: _Optional[_Iterable[_Union[_search_pb2.SearchInventory, _Mapping]]] = ...) -> None: ...
