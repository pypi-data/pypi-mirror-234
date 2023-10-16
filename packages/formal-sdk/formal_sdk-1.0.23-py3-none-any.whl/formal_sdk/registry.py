import grpc


from .gen.admin.v1.registry_pb2 import (
	OnlineInstance,
	OnlineSidecar,
	GetOnlineInstancesByOrgIdRequest,
	GetOnlineInstancesByOrgIdResponse,
	GetOnlineInstancesBySidecarIdRequest,
	GetOnlineInstancesBySidecarIdResponse,
)

from .gen.admin.v1.registry_pb2_grpc import RegistryServiceStub
class RegistryService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = RegistryServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def GetOnlineInstancesByOrgId(self, request: GetOnlineInstancesByOrgIdRequest) -> GetOnlineInstancesByOrgIdResponse:
		return self.stub.GetOnlineInstancesByOrgId(request, metadata=self.headers)

	def GetOnlineInstancesBySidecarId(self, request: GetOnlineInstancesBySidecarIdRequest) -> GetOnlineInstancesBySidecarIdResponse:
		return self.stub.GetOnlineInstancesBySidecarId(request, metadata=self.headers)

