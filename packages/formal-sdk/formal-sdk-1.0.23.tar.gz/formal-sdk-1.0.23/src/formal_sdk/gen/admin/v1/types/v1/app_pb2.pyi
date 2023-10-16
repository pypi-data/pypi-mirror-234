from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IntegrationApp(_message.Message):
    __slots__ = ["id", "name", "type", "created_at", "metabase_hostname", "metabase_username", "metabase_password", "linked_db_user_id", "fivetran_api_key", "fivetran_api_secret"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    METABASE_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    METABASE_USERNAME_FIELD_NUMBER: _ClassVar[int]
    METABASE_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    LINKED_DB_USER_ID_FIELD_NUMBER: _ClassVar[int]
    FIVETRAN_API_KEY_FIELD_NUMBER: _ClassVar[int]
    FIVETRAN_API_SECRET_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    type: str
    created_at: int
    metabase_hostname: str
    metabase_username: str
    metabase_password: str
    linked_db_user_id: str
    fivetran_api_key: str
    fivetran_api_secret: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[str] = ..., created_at: _Optional[int] = ..., metabase_hostname: _Optional[str] = ..., metabase_username: _Optional[str] = ..., metabase_password: _Optional[str] = ..., linked_db_user_id: _Optional[str] = ..., fivetran_api_key: _Optional[str] = ..., fivetran_api_secret: _Optional[str] = ...) -> None: ...
