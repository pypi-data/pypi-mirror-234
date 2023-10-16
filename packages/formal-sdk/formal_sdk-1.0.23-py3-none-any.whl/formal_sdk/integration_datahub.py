import grpc


from .gen.admin.v1.integration_datahub_pb2 import (
	CreateDatahubIntegrationRequest,
	CreateDatahubIntegrationResponse,
	GetDatahubIntegrationRequest,
	GetDatahubIntegrationResponse,
	UpdateDatahubIntegrationRequest,
	UpdateDatahubIntegrationResponse,
	RefreshWebhookTokenRequest,
	RefreshWebhookTokenResponse,
	DeleteDatahubIntegrationRequest,
	DeleteDatahubIntegrationResponse,
)

from .gen.admin.v1.integration_datahub_pb2_grpc import DatahubServiceStub
class DatahubService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = DatahubServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def CreateDatahubIntegration(self, request: CreateDatahubIntegrationRequest) -> CreateDatahubIntegrationResponse:
		return self.stub.CreateDatahubIntegration(request, metadata=self.headers)

	def GetDatahubIntegration(self, request: GetDatahubIntegrationRequest) -> GetDatahubIntegrationResponse:
		return self.stub.GetDatahubIntegration(request, metadata=self.headers)

	def UpdateDatahubIntegration(self, request: UpdateDatahubIntegrationRequest) -> UpdateDatahubIntegrationResponse:
		return self.stub.UpdateDatahubIntegration(request, metadata=self.headers)

	def RefreshWebhookToken(self, request: RefreshWebhookTokenRequest) -> RefreshWebhookTokenResponse:
		return self.stub.RefreshWebhookToken(request, metadata=self.headers)

	def DeleteDatahubIntegration(self, request: DeleteDatahubIntegrationRequest) -> DeleteDatahubIntegrationResponse:
		return self.stub.DeleteDatahubIntegration(request, metadata=self.headers)

