import grpc


from .gen.admin.v1.integration_cloud_pb2 import (
	CreateDataplaneRequest,
	CreateDataplaneResponse,
	GetDataplaneByIdRequest,
	GetDataplaneByIdResponse,
	DeleteDataplaneRequest,
	DeleteDataplaneResponse,
	CreateDataplaneRoutesRequest,
	CreateDataplaneRoutesResponse,
	GetDataplaneRoutesByIdRequest,
	GetDataplaneRoutesByIdResponse,
	DeleteDataplaneRoutesRequest,
	DeleteDataplaneRoutesResponse,
	CreateAwsConnectionSessionRequest,
	CreateAwsConnectionSessionResponse,
	DeleteAwsConnectionSessionRequest,
	GetIntegrationsCloudAccountByIdRequest,
	GetIntegrationsCloudAccountByIdResponse,
	GetIntegrationsCloudAccountsRequest,
	GetIntegrationsCloudAccountsResponse,
	CreateGcpConnectionSessionRequest,
	CreateGcpConnectionSessionResponse,
	DeleteAwsConnectionSessionResponse,
	GetDataplaneStacksByCloudAccountIdRequest,
	GetDataplaneStacksByCloudAccountIdResponse,
)

from .gen.admin.v1.integration_cloud_pb2_grpc import CloudServiceStub
class CloudService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = CloudServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def CreateDataplane(self, request: CreateDataplaneRequest) -> CreateDataplaneResponse:
		return self.stub.CreateDataplane(request, metadata=self.headers)

	def GetDataplaneById(self, request: GetDataplaneByIdRequest) -> GetDataplaneByIdResponse:
		return self.stub.GetDataplaneById(request, metadata=self.headers)

	def DeleteDataplane(self, request: DeleteDataplaneRequest) -> DeleteDataplaneResponse:
		return self.stub.DeleteDataplane(request, metadata=self.headers)

	def CreateDataplaneRoutes(self, request: CreateDataplaneRoutesRequest) -> CreateDataplaneRoutesResponse:
		return self.stub.CreateDataplaneRoutes(request, metadata=self.headers)

	def GetDataplaneRoutesById(self, request: GetDataplaneRoutesByIdRequest) -> GetDataplaneRoutesByIdResponse:
		return self.stub.GetDataplaneRoutesById(request, metadata=self.headers)

	def DeleteDataplaneRoutes(self, request: DeleteDataplaneRoutesRequest) -> DeleteDataplaneRoutesResponse:
		return self.stub.DeleteDataplaneRoutes(request, metadata=self.headers)

	def GetDataplaneStacksByCloudAccountId(self, request: GetDataplaneStacksByCloudAccountIdRequest) -> GetDataplaneStacksByCloudAccountIdResponse:
		return self.stub.GetDataplaneStacksByCloudAccountId(request, metadata=self.headers)

	def CreateAwsConnectionSession(self, request: CreateAwsConnectionSessionRequest) -> CreateAwsConnectionSessionResponse:
		return self.stub.CreateAwsConnectionSession(request, metadata=self.headers)

	def DeleteAwsConnectionSession(self, request: DeleteAwsConnectionSessionRequest) -> DeleteAwsConnectionSessionResponse:
		return self.stub.DeleteAwsConnectionSession(request, metadata=self.headers)

	def GetIntegrationsCloudAccountById(self, request: GetIntegrationsCloudAccountByIdRequest) -> GetIntegrationsCloudAccountByIdResponse:
		return self.stub.GetIntegrationsCloudAccountById(request, metadata=self.headers)

	def GetIntegrationsCloudAccounts(self, request: GetIntegrationsCloudAccountsRequest) -> GetIntegrationsCloudAccountsResponse:
		return self.stub.GetIntegrationsCloudAccounts(request, metadata=self.headers)

	def CreateGcpConnectionSession(self, request: CreateGcpConnectionSessionRequest) -> CreateGcpConnectionSessionResponse:
		return self.stub.CreateGcpConnectionSession(request, metadata=self.headers)

