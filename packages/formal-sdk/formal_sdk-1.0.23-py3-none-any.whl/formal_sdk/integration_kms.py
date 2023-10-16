import grpc


from .gen.admin.v1.integration_kms_pb2 import (
	CreateKeyRegistrationRequest,
	CreateKeyRegistrationResponse,
	GetKeysRequest,
	GetKeysResponse,
	GetKeyRequest,
	GetKeyResponse,
	DeactivateFieldEncryptionKeyRequest,
	DeactivateFieldEncryptionKeyResponse,
)

from .gen.admin.v1.integration_kms_pb2_grpc import KmsServiceStub
class KmsService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = KmsServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def CreateKeyRegistration(self, request: CreateKeyRegistrationRequest) -> CreateKeyRegistrationResponse:
		return self.stub.CreateKeyRegistration(request, metadata=self.headers)

	def GetKeys(self, request: GetKeysRequest) -> GetKeysResponse:
		return self.stub.GetKeys(request, metadata=self.headers)

	def GetKey(self, request: GetKeyRequest) -> GetKeyResponse:
		return self.stub.GetKey(request, metadata=self.headers)

	def DeactivateFieldEncryptionKey(self, request: DeactivateFieldEncryptionKeyRequest) -> DeactivateFieldEncryptionKeyResponse:
		return self.stub.DeactivateFieldEncryptionKey(request, metadata=self.headers)

