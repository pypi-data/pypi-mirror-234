from .types.v1 import coderepo_pb2 as _coderepo_pb2
from .types.v1 import github_repository_pb2 as _github_repository_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeleteCodeRepoByIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteCodeRepoByIdResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CancelDeleteCodeRepoByIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class CancelDeleteCodeRepoByIdResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ConnectCodeRepositoryRequest(_message.Message):
    __slots__ = ["user_id", "type", "code"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    type: str
    code: str
    def __init__(self, user_id: _Optional[str] = ..., type: _Optional[str] = ..., code: _Optional[str] = ...) -> None: ...

class ConnectCodeRepositoryResponse(_message.Message):
    __slots__ = ["access_token"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    def __init__(self, access_token: _Optional[str] = ...) -> None: ...

class GetAccessTokenRequest(_message.Message):
    __slots__ = ["user_id", "type"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    type: str
    def __init__(self, user_id: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class GetAccessTokenResponse(_message.Message):
    __slots__ = ["access_token"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    def __init__(self, access_token: _Optional[str] = ...) -> None: ...

class GetGithubRepositoriesFromAuthUserRequest(_message.Message):
    __slots__ = ["user_id"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class GetGithubRepositoriesFromAuthUserResponse(_message.Message):
    __slots__ = ["repositories"]
    REPOSITORIES_FIELD_NUMBER: _ClassVar[int]
    repositories: _containers.RepeatedCompositeFieldContainer[_github_repository_pb2.GithubRepository]
    def __init__(self, repositories: _Optional[_Iterable[_Union[_github_repository_pb2.GithubRepository, _Mapping]]] = ...) -> None: ...

class GetUserAccessTokenRequest(_message.Message):
    __slots__ = ["user_id"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class GetUserAccessTokenResponse(_message.Message):
    __slots__ = ["access_token"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    def __init__(self, access_token: _Optional[str] = ...) -> None: ...

class GetCodeReposRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetCodeReposResponse(_message.Message):
    __slots__ = ["repositories"]
    REPOSITORIES_FIELD_NUMBER: _ClassVar[int]
    repositories: _containers.RepeatedCompositeFieldContainer[_coderepo_pb2.CodeRepo]
    def __init__(self, repositories: _Optional[_Iterable[_Union[_coderepo_pb2.CodeRepo, _Mapping]]] = ...) -> None: ...

class CreateCodeRepoRequest(_message.Message):
    __slots__ = ["repository"]
    REPOSITORY_FIELD_NUMBER: _ClassVar[int]
    repository: _coderepo_pb2.CodeRepo
    def __init__(self, repository: _Optional[_Union[_coderepo_pb2.CodeRepo, _Mapping]] = ...) -> None: ...

class CreateCodeRepoResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
