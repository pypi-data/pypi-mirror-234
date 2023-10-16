from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LogLinkItem(_message.Message):
    __slots__ = ["id", "integration_log_id", "datastore_id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_LOG_ID_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    integration_log_id: str
    datastore_id: str
    def __init__(self, id: _Optional[str] = ..., integration_log_id: _Optional[str] = ..., datastore_id: _Optional[str] = ...) -> None: ...
