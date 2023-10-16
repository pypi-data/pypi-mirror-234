from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OnlineInstance(_message.Message):
    __slots__ = ["instance_id", "last_seen", "start_time", "version"]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_SEEN_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    instance_id: str
    last_seen: _timestamp_pb2.Timestamp
    start_time: _timestamp_pb2.Timestamp
    version: str
    def __init__(self, instance_id: _Optional[str] = ..., last_seen: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., version: _Optional[str] = ...) -> None: ...

class OnlineSidecar(_message.Message):
    __slots__ = ["sidecar_id", "instances"]
    SIDECAR_ID_FIELD_NUMBER: _ClassVar[int]
    INSTANCES_FIELD_NUMBER: _ClassVar[int]
    sidecar_id: str
    instances: _containers.RepeatedCompositeFieldContainer[OnlineInstance]
    def __init__(self, sidecar_id: _Optional[str] = ..., instances: _Optional[_Iterable[_Union[OnlineInstance, _Mapping]]] = ...) -> None: ...

class GetOnlineInstancesByOrgIdRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetOnlineInstancesByOrgIdResponse(_message.Message):
    __slots__ = ["sidecars"]
    class SidecarsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: OnlineSidecar
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[OnlineSidecar, _Mapping]] = ...) -> None: ...
    SIDECARS_FIELD_NUMBER: _ClassVar[int]
    sidecars: _containers.MessageMap[str, OnlineSidecar]
    def __init__(self, sidecars: _Optional[_Mapping[str, OnlineSidecar]] = ...) -> None: ...

class GetOnlineInstancesBySidecarIdRequest(_message.Message):
    __slots__ = ["sidecar_id"]
    SIDECAR_ID_FIELD_NUMBER: _ClassVar[int]
    sidecar_id: str
    def __init__(self, sidecar_id: _Optional[str] = ...) -> None: ...

class GetOnlineInstancesBySidecarIdResponse(_message.Message):
    __slots__ = ["instances"]
    INSTANCES_FIELD_NUMBER: _ClassVar[int]
    instances: _containers.RepeatedCompositeFieldContainer[OnlineInstance]
    def __init__(self, instances: _Optional[_Iterable[_Union[OnlineInstance, _Mapping]]] = ...) -> None: ...
