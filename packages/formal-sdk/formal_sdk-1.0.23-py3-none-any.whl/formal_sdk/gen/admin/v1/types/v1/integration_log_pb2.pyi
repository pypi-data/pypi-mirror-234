from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IntegrationLogs(_message.Message):
    __slots__ = ["id", "name", "type", "created_at", "dd_site", "dd_account_id", "splunk_url"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DD_SITE_FIELD_NUMBER: _ClassVar[int]
    DD_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SPLUNK_URL_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    type: str
    created_at: int
    dd_site: str
    dd_account_id: str
    splunk_url: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[str] = ..., created_at: _Optional[int] = ..., dd_site: _Optional[str] = ..., dd_account_id: _Optional[str] = ..., splunk_url: _Optional[str] = ...) -> None: ...
