from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetClientAuthTokenRequest(_message.Message):
    __slots__ = ["user_id", "user_name", "user_email"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    user_name: str
    user_email: str
    def __init__(self, user_id: _Optional[str] = ..., user_name: _Optional[str] = ..., user_email: _Optional[str] = ...) -> None: ...

class GetClientAuthTokenResponse(_message.Message):
    __slots__ = ["token"]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...
