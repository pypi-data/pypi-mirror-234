from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Satellite(_message.Message):
    __slots__ = ["id", "tls_cert", "name", "status"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TLS_CERT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    tls_cert: str
    name: str
    status: str
    def __init__(self, id: _Optional[str] = ..., tls_cert: _Optional[str] = ..., name: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...
