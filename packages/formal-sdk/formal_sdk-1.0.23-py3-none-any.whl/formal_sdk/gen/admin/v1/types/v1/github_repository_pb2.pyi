from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GithubRepository(_message.Message):
    __slots__ = ["id", "full_name", "html_url"]
    ID_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    HTML_URL_FIELD_NUMBER: _ClassVar[int]
    id: int
    full_name: str
    html_url: str
    def __init__(self, id: _Optional[int] = ..., full_name: _Optional[str] = ..., html_url: _Optional[str] = ...) -> None: ...
