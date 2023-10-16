from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CreateSlackIntegrationRequest(_message.Message):
    __slots__ = ["code", "redirect_uri"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    code: str
    redirect_uri: str
    def __init__(self, code: _Optional[str] = ..., redirect_uri: _Optional[str] = ...) -> None: ...

class CreateSlackIntegrationResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetSlackIntegrationRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetSlackIntegrationResponse(_message.Message):
    __slots__ = ["team_id", "team_name", "bot_user_id", "bot_access_token", "authed_user_id", "channel_id"]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    BOT_USER_ID_FIELD_NUMBER: _ClassVar[int]
    BOT_ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    AUTHED_USER_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    team_name: str
    bot_user_id: str
    bot_access_token: str
    authed_user_id: str
    channel_id: str
    def __init__(self, team_id: _Optional[str] = ..., team_name: _Optional[str] = ..., bot_user_id: _Optional[str] = ..., bot_access_token: _Optional[str] = ..., authed_user_id: _Optional[str] = ..., channel_id: _Optional[str] = ...) -> None: ...
