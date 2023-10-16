from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class InstallGithubAppRequest(_message.Message):
    __slots__ = ["installation_id"]
    INSTALLATION_ID_FIELD_NUMBER: _ClassVar[int]
    installation_id: str
    def __init__(self, installation_id: _Optional[str] = ...) -> None: ...

class InstallGithubAppResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetGithubAppForOrgRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetGithubAppForOrgResponse(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
