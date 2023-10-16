from .types.v1 import flat_dataplane_pb2 as _flat_dataplane_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateDataplaneRequest(_message.Message):
    __slots__ = ["name", "region", "cloud_account_id", "availability_zone", "vpc_peering"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    CLOUD_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    AVAILABILITY_ZONE_FIELD_NUMBER: _ClassVar[int]
    VPC_PEERING_FIELD_NUMBER: _ClassVar[int]
    name: str
    region: str
    cloud_account_id: str
    availability_zone: int
    vpc_peering: bool
    def __init__(self, name: _Optional[str] = ..., region: _Optional[str] = ..., cloud_account_id: _Optional[str] = ..., availability_zone: _Optional[int] = ..., vpc_peering: bool = ...) -> None: ...

class CreateDataplaneResponse(_message.Message):
    __slots__ = ["dataplane"]
    DATAPLANE_FIELD_NUMBER: _ClassVar[int]
    dataplane: _flat_dataplane_pb2.FlatDataplane
    def __init__(self, dataplane: _Optional[_Union[_flat_dataplane_pb2.FlatDataplane, _Mapping]] = ...) -> None: ...

class GetDataplaneByIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetDataplaneByIdResponse(_message.Message):
    __slots__ = ["dataplane"]
    DATAPLANE_FIELD_NUMBER: _ClassVar[int]
    dataplane: _flat_dataplane_pb2.FlatDataplane
    def __init__(self, dataplane: _Optional[_Union[_flat_dataplane_pb2.FlatDataplane, _Mapping]] = ...) -> None: ...

class DeleteDataplaneRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteDataplaneResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CreateDataplaneRoutesRequest(_message.Message):
    __slots__ = ["dataplane_id", "destination_cidr_block", "transit_gateway_id", "vpc_peering_connection_id"]
    DATAPLANE_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_CIDR_BLOCK_FIELD_NUMBER: _ClassVar[int]
    TRANSIT_GATEWAY_ID_FIELD_NUMBER: _ClassVar[int]
    VPC_PEERING_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    dataplane_id: str
    destination_cidr_block: str
    transit_gateway_id: str
    vpc_peering_connection_id: str
    def __init__(self, dataplane_id: _Optional[str] = ..., destination_cidr_block: _Optional[str] = ..., transit_gateway_id: _Optional[str] = ..., vpc_peering_connection_id: _Optional[str] = ...) -> None: ...

class CreateDataplaneRoutesResponse(_message.Message):
    __slots__ = ["dataplane_routes"]
    DATAPLANE_ROUTES_FIELD_NUMBER: _ClassVar[int]
    dataplane_routes: _flat_dataplane_pb2.DataplaneTransitGatewayRoutes
    def __init__(self, dataplane_routes: _Optional[_Union[_flat_dataplane_pb2.DataplaneTransitGatewayRoutes, _Mapping]] = ...) -> None: ...

class GetDataplaneRoutesByIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetDataplaneRoutesByIdResponse(_message.Message):
    __slots__ = ["dataplane_routes"]
    DATAPLANE_ROUTES_FIELD_NUMBER: _ClassVar[int]
    dataplane_routes: _flat_dataplane_pb2.DataplaneTransitGatewayRoutes
    def __init__(self, dataplane_routes: _Optional[_Union[_flat_dataplane_pb2.DataplaneTransitGatewayRoutes, _Mapping]] = ...) -> None: ...

class DeleteDataplaneRoutesRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteDataplaneRoutesResponse(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class CreateAwsConnectionSessionRequest(_message.Message):
    __slots__ = ["cloud_account_name", "cloud_account_region"]
    CLOUD_ACCOUNT_NAME_FIELD_NUMBER: _ClassVar[int]
    CLOUD_ACCOUNT_REGION_FIELD_NUMBER: _ClassVar[int]
    cloud_account_name: str
    cloud_account_region: str
    def __init__(self, cloud_account_name: _Optional[str] = ..., cloud_account_region: _Optional[str] = ...) -> None: ...

class CreateAwsConnectionSessionResponse(_message.Message):
    __slots__ = ["cloud_integration"]
    CLOUD_INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    cloud_integration: _flat_dataplane_pb2.CloudIntegration
    def __init__(self, cloud_integration: _Optional[_Union[_flat_dataplane_pb2.CloudIntegration, _Mapping]] = ...) -> None: ...

class DeleteAwsConnectionSessionRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetIntegrationsCloudAccountByIdRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetIntegrationsCloudAccountByIdResponse(_message.Message):
    __slots__ = ["integration"]
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: _flat_dataplane_pb2.CloudIntegration
    def __init__(self, integration: _Optional[_Union[_flat_dataplane_pb2.CloudIntegration, _Mapping]] = ...) -> None: ...

class GetIntegrationsCloudAccountsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetIntegrationsCloudAccountsResponse(_message.Message):
    __slots__ = ["integrations"]
    INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    integrations: _containers.RepeatedCompositeFieldContainer[_flat_dataplane_pb2.CloudIntegration]
    def __init__(self, integrations: _Optional[_Iterable[_Union[_flat_dataplane_pb2.CloudIntegration, _Mapping]]] = ...) -> None: ...

class CreateGcpConnectionSessionRequest(_message.Message):
    __slots__ = ["project_id"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class CreateGcpConnectionSessionResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteAwsConnectionSessionResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetDataplaneStacksByCloudAccountIdRequest(_message.Message):
    __slots__ = ["cloud_account_id"]
    CLOUD_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    cloud_account_id: str
    def __init__(self, cloud_account_id: _Optional[str] = ...) -> None: ...

class GetDataplaneStacksByCloudAccountIdResponse(_message.Message):
    __slots__ = ["dataplanes"]
    DATAPLANES_FIELD_NUMBER: _ClassVar[int]
    dataplanes: _containers.RepeatedCompositeFieldContainer[_flat_dataplane_pb2.FlatDataplane]
    def __init__(self, dataplanes: _Optional[_Iterable[_Union[_flat_dataplane_pb2.FlatDataplane, _Mapping]]] = ...) -> None: ...
