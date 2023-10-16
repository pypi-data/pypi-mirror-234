import grpc


from .gen.admin.v1.integration_log_pb2 import (
	CreateIntegrationLogsRequest,
	CreateIntegrationLogsResponse,
	GetIntegrationLogsRequest,
	GetIntegrationLogsResponse,
	GetIntegrationLogByIdRequest,
	GetIntegrationLogByIdResponse,
	DeleteIntegrationLogsRequest,
	DeleteIntegrationLogsResponse,
	CreateLogsLinkItemRequest,
	CreateLogsLinkItemResponse,
	GetLogsLinkItemByIdRequest,
	GetLogsLinkItemByIdResponse,
	DeleteLogsLinkItemRequest,
	DeleteLogsLinkItemResponse,
)

from .gen.admin.v1.integration_log_pb2_grpc import LogsServiceStub
class LogsService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = LogsServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def CreateIntegrationLogs(self, request: CreateIntegrationLogsRequest) -> CreateIntegrationLogsResponse:
		return self.stub.CreateIntegrationLogs(request, metadata=self.headers)

	def GetIntegrationLogs(self, request: GetIntegrationLogsRequest) -> GetIntegrationLogsResponse:
		return self.stub.GetIntegrationLogs(request, metadata=self.headers)

	def GetIntegrationLogById(self, request: GetIntegrationLogByIdRequest) -> GetIntegrationLogByIdResponse:
		return self.stub.GetIntegrationLogById(request, metadata=self.headers)

	def DeleteIntegrationLogs(self, request: DeleteIntegrationLogsRequest) -> DeleteIntegrationLogsResponse:
		return self.stub.DeleteIntegrationLogs(request, metadata=self.headers)

	def CreateLogsLinkItem(self, request: CreateLogsLinkItemRequest) -> CreateLogsLinkItemResponse:
		return self.stub.CreateLogsLinkItem(request, metadata=self.headers)

	def GetLogsLinkItemById(self, request: GetLogsLinkItemByIdRequest) -> GetLogsLinkItemByIdResponse:
		return self.stub.GetLogsLinkItemById(request, metadata=self.headers)

	def DeleteLogsLinkItem(self, request: DeleteLogsLinkItemRequest) -> DeleteLogsLinkItemResponse:
		return self.stub.DeleteLogsLinkItem(request, metadata=self.headers)

