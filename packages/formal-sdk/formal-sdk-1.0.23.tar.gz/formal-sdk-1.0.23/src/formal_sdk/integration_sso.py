import grpc


from .gen.admin.v1.integration_sso_pb2 import (
	GetWorkOsOrgRequest,
	GetWorkOsOrgResponse,
	UpdateWorkOsOrgRequest,
	UpdateWorkOsOrgResponse,
	GetSsoConnectionsRequest,
	GetSsoConnectionsResponse,
	DeleteConnectionRequest,
	DeleteConnectionResponse,
)

from .gen.admin.v1.integration_sso_pb2_grpc import SsoServiceStub
class SsoService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = SsoServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def GetWorkOsOrg(self, request: GetWorkOsOrgRequest) -> GetWorkOsOrgResponse:
		return self.stub.GetWorkOsOrg(request, metadata=self.headers)

	def UpdateWorkOsOrg(self, request: UpdateWorkOsOrgRequest) -> UpdateWorkOsOrgResponse:
		return self.stub.UpdateWorkOsOrg(request, metadata=self.headers)

	def GetSsoConnections(self, request: GetSsoConnectionsRequest) -> GetSsoConnectionsResponse:
		return self.stub.GetSsoConnections(request, metadata=self.headers)

	def DeleteConnection(self, request: DeleteConnectionRequest) -> DeleteConnectionResponse:
		return self.stub.DeleteConnection(request, metadata=self.headers)

