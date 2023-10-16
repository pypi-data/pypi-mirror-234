from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ListMetadata(_message.Message):
    __slots__ = ["after", "before", "count", "next_cursor"]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    after: str
    before: str
    count: int
    next_cursor: str
    def __init__(self, after: _Optional[str] = ..., before: _Optional[str] = ..., count: _Optional[int] = ..., next_cursor: _Optional[str] = ...) -> None: ...
