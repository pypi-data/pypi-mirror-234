import grpc


from .gen.admin.v1.integration_external_api_pb2 import (
	Auth,
	CreateExternalApiIntegrationRequest,
	CreateExternalApiIntegrationResponse,
	ApiIntegration,
	GetExternalApiIntegrationRequest,
	GetExternalApiIntegrationResponse,
	DeleteExternalApiIntegrationRequest,
	DeleteExternalApiIntegrationResponse,
	GetExternalApiIntegrationsRequest,
	GetExternalApiIntegrationsResponse,
)

from .gen.admin.v1.integration_external_api_pb2_grpc import ExternalApiServiceStub
class ExternalApiService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = ExternalApiServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def CreateExternalApiIntegration(self, request: CreateExternalApiIntegrationRequest) -> CreateExternalApiIntegrationResponse:
		return self.stub.CreateExternalApiIntegration(request, metadata=self.headers)

	def GetExternalApiIntegration(self, request: GetExternalApiIntegrationRequest) -> GetExternalApiIntegrationResponse:
		return self.stub.GetExternalApiIntegration(request, metadata=self.headers)

	def DeleteExternalApiIntegration(self, request: DeleteExternalApiIntegrationRequest) -> DeleteExternalApiIntegrationResponse:
		return self.stub.DeleteExternalApiIntegration(request, metadata=self.headers)

	def GetExternalApiIntegrations(self, request: GetExternalApiIntegrationsRequest) -> GetExternalApiIntegrationsResponse:
		return self.stub.GetExternalApiIntegrations(request, metadata=self.headers)

