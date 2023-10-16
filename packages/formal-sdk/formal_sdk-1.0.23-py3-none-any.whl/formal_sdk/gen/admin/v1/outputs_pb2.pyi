from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetOutputsRequest(_message.Message):
    __slots__ = ["item_id"]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    item_id: str
    def __init__(self, item_id: _Optional[str] = ...) -> None: ...

class GetOutputsResponse(_message.Message):
    __slots__ = ["records"]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    records: _containers.RepeatedCompositeFieldContainer[OutputRecord]
    def __init__(self, records: _Optional[_Iterable[_Union[OutputRecord, _Mapping]]] = ...) -> None: ...

class OutputRecord(_message.Message):
    __slots__ = ["id", "item_id", "message", "created_at", "log_level"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    LOG_LEVEL_FIELD_NUMBER: _ClassVar[int]
    id: str
    item_id: str
    message: str
    created_at: _timestamp_pb2.Timestamp
    log_level: str
    def __init__(self, id: _Optional[str] = ..., item_id: _Optional[str] = ..., message: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., log_level: _Optional[str] = ...) -> None: ...
