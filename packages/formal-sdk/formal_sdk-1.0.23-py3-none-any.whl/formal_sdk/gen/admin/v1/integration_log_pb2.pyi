from .types.v1 import integration_log_pb2 as _integration_log_pb2
from .types.v1 import log_link_pb2 as _log_link_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateIntegrationLogsRequest(_message.Message):
    __slots__ = ["name", "type", "dd_site", "dd_api_key", "dd_account_id", "splunk_url", "splunk_api_key"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DD_SITE_FIELD_NUMBER: _ClassVar[int]
    DD_API_KEY_FIELD_NUMBER: _ClassVar[int]
    DD_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SPLUNK_URL_FIELD_NUMBER: _ClassVar[int]
    SPLUNK_API_KEY_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: str
    dd_site: str
    dd_api_key: str
    dd_account_id: str
    splunk_url: str
    splunk_api_key: str
    def __init__(self, name: _Optional[str] = ..., type: _Optional[str] = ..., dd_site: _Optional[str] = ..., dd_api_key: _Optional[str] = ..., dd_account_id: _Optional[str] = ..., splunk_url: _Optional[str] = ..., splunk_api_key: _Optional[str] = ...) -> None: ...

class CreateIntegrationLogsResponse(_message.Message):
    __slots__ = ["integration"]
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: _integration_log_pb2.IntegrationLogs
    def __init__(self, integration: _Optional[_Union[_integration_log_pb2.IntegrationLogs, _Mapping]] = ...) -> None: ...

class GetIntegrationLogsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetIntegrationLogsResponse(_message.Message):
    __slots__ = ["integrations"]
    INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    integrations: _containers.RepeatedCompositeFieldContainer[_integration_log_pb2.IntegrationLogs]
    def __init__(self, integrations: _Optional[_Iterable[_Union[_integration_log_pb2.IntegrationLogs, _Mapping]]] = ...) -> None: ...

class GetIntegrationLogByIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetIntegrationLogByIdResponse(_message.Message):
    __slots__ = ["integration"]
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: _integration_log_pb2.IntegrationLogs
    def __init__(self, integration: _Optional[_Union[_integration_log_pb2.IntegrationLogs, _Mapping]] = ...) -> None: ...

class DeleteIntegrationLogsRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteIntegrationLogsResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CreateLogsLinkItemRequest(_message.Message):
    __slots__ = ["integration_id", "datastore_id"]
    INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    integration_id: str
    datastore_id: str
    def __init__(self, integration_id: _Optional[str] = ..., datastore_id: _Optional[str] = ...) -> None: ...

class CreateLogsLinkItemResponse(_message.Message):
    __slots__ = ["log_item_link"]
    LOG_ITEM_LINK_FIELD_NUMBER: _ClassVar[int]
    log_item_link: _log_link_pb2.LogLinkItem
    def __init__(self, log_item_link: _Optional[_Union[_log_link_pb2.LogLinkItem, _Mapping]] = ...) -> None: ...

class GetLogsLinkItemByIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetLogsLinkItemByIdResponse(_message.Message):
    __slots__ = ["log_item_links"]
    LOG_ITEM_LINKS_FIELD_NUMBER: _ClassVar[int]
    log_item_links: _log_link_pb2.LogLinkItem
    def __init__(self, log_item_links: _Optional[_Union[_log_link_pb2.LogLinkItem, _Mapping]] = ...) -> None: ...

class DeleteLogsLinkItemRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteLogsLinkItemResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
