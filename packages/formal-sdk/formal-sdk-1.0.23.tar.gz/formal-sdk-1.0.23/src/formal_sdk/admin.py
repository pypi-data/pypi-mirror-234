import grpc


from .gen.admin.v1.admin_pb2 import (
	GetApiKeysRequest,
	ApiKey,
	GetApiKeysResponse,
	CreateApiKeyRequest,
	CreateApiKeyResponse,
	DeleteApiKeyRequest,
	DeleteApiKeyResponse,
)

from .gen.admin.v1.admin_pb2_grpc import DevServiceStub
class DevService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = DevServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def GetApiKeys(self, request: GetApiKeysRequest) -> GetApiKeysResponse:
		return self.stub.GetApiKeys(request, metadata=self.headers)

	def CreateApiKey(self, request: CreateApiKeyRequest) -> CreateApiKeyResponse:
		return self.stub.CreateApiKey(request, metadata=self.headers)

	def DeleteApiKey(self, request: DeleteApiKeyRequest) -> DeleteApiKeyResponse:
		return self.stub.DeleteApiKey(request, metadata=self.headers)

