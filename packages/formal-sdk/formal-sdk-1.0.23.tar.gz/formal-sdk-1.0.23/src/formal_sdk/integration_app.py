import grpc


from .gen.admin.v1.integration_app_pb2 import (
	RefreshIntegrationAppsRequest,
	RefreshIntegrationAppsResponse,
	GetIntegrationAppsRequest,
	GetIntegrationAppsResponse,
	GetIntegrationByIdRequest,
	GetIntegrationByIdResponse,
	CreateIntegrationAppRequest,
	CreateIntegrationAppResponse,
	DeleteIntegrationAppRequest,
	DeleteIntegrationAppResponse,
)

from .gen.admin.v1.integration_app_pb2_grpc import AppServiceStub
class AppService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = AppServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def RefreshIntegrationApps(self, request: RefreshIntegrationAppsRequest) -> RefreshIntegrationAppsResponse:
		return self.stub.RefreshIntegrationApps(request, metadata=self.headers)

	def GetIntegrationApps(self, request: GetIntegrationAppsRequest) -> GetIntegrationAppsResponse:
		return self.stub.GetIntegrationApps(request, metadata=self.headers)

	def GetIntegrationById(self, request: GetIntegrationByIdRequest) -> GetIntegrationByIdResponse:
		return self.stub.GetIntegrationById(request, metadata=self.headers)

	def CreateIntegrationApp(self, request: CreateIntegrationAppRequest) -> CreateIntegrationAppResponse:
		return self.stub.CreateIntegrationApp(request, metadata=self.headers)

	def DeleteIntegrationApp(self, request: DeleteIntegrationAppRequest) -> DeleteIntegrationAppResponse:
		return self.stub.DeleteIntegrationApp(request, metadata=self.headers)

