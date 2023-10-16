import grpc


from .gen.admin.v1.encryption_pb2 import (
	CreateOrUpdateDefaultFieldEncryptionPolicyRequest,
	CreateOrUpdateDefaultFieldEncryptionPolicyResponse,
	GetDefaultFieldEncryptionPolicyRequest,
	GetDefaultFieldEncryptionPolicyResponse,
	DefaultFieldEncryptionPolicy,
	CreateFieldEncryptionRequest,
	CreateFieldEncryptionResponse,
	GetFieldEncryptionsByDatastoreRequest,
	GetFieldEncryptionsByDatastoreResponse,
	DeleteFieldEncryptionRequest,
	DeleteFieldEncryptionResponse,
	FieldEncryption,
)

from .gen.admin.v1.encryption_pb2_grpc import FieldEncryptionPolicyServiceStub
class FieldEncryptionPolicyService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = FieldEncryptionPolicyServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def CreateOrUpdateDefaultFieldEncryptionPolicy(self, request: CreateOrUpdateDefaultFieldEncryptionPolicyRequest) -> CreateOrUpdateDefaultFieldEncryptionPolicyResponse:
		return self.stub.CreateOrUpdateDefaultFieldEncryptionPolicy(request, metadata=self.headers)

	def GetDefaultFieldEncryptionPolicy(self, request: GetDefaultFieldEncryptionPolicyRequest) -> GetDefaultFieldEncryptionPolicyResponse:
		return self.stub.GetDefaultFieldEncryptionPolicy(request, metadata=self.headers)

from .gen.admin.v1.encryption_pb2_grpc import FieldEncryptionServiceStub
class FieldEncryptionService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = FieldEncryptionServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def CreateFieldEncryption(self, request: CreateFieldEncryptionRequest) -> CreateFieldEncryptionResponse:
		return self.stub.CreateFieldEncryption(request, metadata=self.headers)

	def GetFieldEncryptionsByDatastore(self, request: GetFieldEncryptionsByDatastoreRequest) -> GetFieldEncryptionsByDatastoreResponse:
		return self.stub.GetFieldEncryptionsByDatastore(request, metadata=self.headers)

	def DeleteFieldEncryption(self, request: DeleteFieldEncryptionRequest) -> DeleteFieldEncryptionResponse:
		return self.stub.DeleteFieldEncryption(request, metadata=self.headers)

