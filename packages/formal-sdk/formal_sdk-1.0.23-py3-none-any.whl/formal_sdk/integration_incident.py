import grpc


from .gen.admin.v1.integration_incident_pb2 import (
	DeleteIncidentAccountByIdRequest,
	DeleteIncidentAccountByIdResponse,
	ConnectIncidentAccountRequest,
	ConnectIncidentAccountResponse,
	GetIncidentAccountsRequest,
	GetIncidentAccountsResponse,
	GetIncidentAccountByIdRequest,
	GetIncidentAccountByIdResponse,
)

from .gen.admin.v1.integration_incident_pb2_grpc import IncidentServiceStub
class IncidentService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = IncidentServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def ConnectIncidentAccount(self, request: ConnectIncidentAccountRequest) -> ConnectIncidentAccountResponse:
		return self.stub.ConnectIncidentAccount(request, metadata=self.headers)

	def GetIncidentAccounts(self, request: GetIncidentAccountsRequest) -> GetIncidentAccountsResponse:
		return self.stub.GetIncidentAccounts(request, metadata=self.headers)

	def GetIncidentAccountById(self, request: GetIncidentAccountByIdRequest) -> GetIncidentAccountByIdResponse:
		return self.stub.GetIncidentAccountById(request, metadata=self.headers)

	def DeleteIncidentAccountById(self, request: DeleteIncidentAccountByIdRequest) -> DeleteIncidentAccountByIdResponse:
		return self.stub.DeleteIncidentAccountById(request, metadata=self.headers)

