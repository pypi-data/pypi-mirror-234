from .types.v1 import log_pb2 as _log_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetLogsRequest(_message.Message):
    __slots__ = ["limit", "offset", "filter"]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    limit: int
    offset: int
    filter: str
    def __init__(self, limit: _Optional[int] = ..., offset: _Optional[int] = ..., filter: _Optional[str] = ...) -> None: ...

class GetLogByIDRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetLogsResponse(_message.Message):
    __slots__ = ["logs", "has_more"]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[_log_pb2.FormalLog]
    has_more: bool
    def __init__(self, logs: _Optional[_Iterable[_Union[_log_pb2.FormalLog, _Mapping]]] = ..., has_more: bool = ...) -> None: ...

class GetLogByIDResponse(_message.Message):
    __slots__ = ["log"]
    LOG_FIELD_NUMBER: _ClassVar[int]
    log: _log_pb2.FormalLog
    def __init__(self, log: _Optional[_Union[_log_pb2.FormalLog, _Mapping]] = ...) -> None: ...

class GetEventBySessionRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetEventBySessionResponse(_message.Message):
    __slots__ = ["event_data"]
    EVENT_DATA_FIELD_NUMBER: _ClassVar[int]
    event_data: _containers.RepeatedCompositeFieldContainer[EventData]
    def __init__(self, event_data: _Optional[_Iterable[_Union[EventData, _Mapping]]] = ...) -> None: ...

class EventData(_message.Message):
    __slots__ = ["timestamp", "type", "session_id", "bytes", "offset"]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    type: str
    session_id: str
    bytes: int
    offset: int
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., type: _Optional[str] = ..., session_id: _Optional[str] = ..., bytes: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class GetDataBySessionRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class SshData(_message.Message):
    __slots__ = ["timestamp", "data", "message_type"]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    data: bytes
    message_type: str
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., data: _Optional[bytes] = ..., message_type: _Optional[str] = ...) -> None: ...

class GetDataBySessionResponse(_message.Message):
    __slots__ = ["ssh_data"]
    SSH_DATA_FIELD_NUMBER: _ClassVar[int]
    ssh_data: _containers.RepeatedCompositeFieldContainer[SshData]
    def __init__(self, ssh_data: _Optional[_Iterable[_Union[SshData, _Mapping]]] = ...) -> None: ...
