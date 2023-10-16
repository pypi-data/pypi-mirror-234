import grpc


from .gen.admin.v1.native_user_pb2 import (
	CreateNativeUserRequest,
	CreateNativeUserResponse,
	GetNativeUsersRequest,
	GetNativeUsersResponse,
	GetNativeUserRequest,
	GetNativeUserResponse,
	NativeUser,
	DeleteNativeUserRequest,
	DeleteNativeUserResponse,
	UpdateNativeUserSecretRequest,
	UpdateNativeUserSecretResponse,
	SetNativeUserAsDefaultRequest,
	SetNativeUserAsDefaultResponse,
	CreateNativeUserIdentityLinkRequest,
	CreateNativeUserIdentityLinkResponse,
	GetNativeUserIdentityLinkRequest,
	CreateNativeUserIdentityLinkV2Request,
	CreateNativeUserIdentityLinkV2Response,
	GetNativeUserIdentityLinkResponse,
	DeleteNativeUserIdentityLinkRequest,
	DeleteNativeUserIdentityLinkResponse,
	NativeUserLink,
)

from .gen.admin.v1.native_user_pb2_grpc import NativeUserServiceStub
class NativeUserService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = NativeUserServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def CreateNativeUser(self, request: CreateNativeUserRequest) -> CreateNativeUserResponse:
		return self.stub.CreateNativeUser(request, metadata=self.headers)

	def GetNativeUser(self, request: GetNativeUserRequest) -> GetNativeUserResponse:
		return self.stub.GetNativeUser(request, metadata=self.headers)

	def GetNativeUsers(self, request: GetNativeUsersRequest) -> GetNativeUsersResponse:
		return self.stub.GetNativeUsers(request, metadata=self.headers)

	def DeleteNativeUser(self, request: DeleteNativeUserRequest) -> DeleteNativeUserResponse:
		return self.stub.DeleteNativeUser(request, metadata=self.headers)

	def UpdateNativeUserSecret(self, request: UpdateNativeUserSecretRequest) -> UpdateNativeUserSecretResponse:
		return self.stub.UpdateNativeUserSecret(request, metadata=self.headers)

	def SetNativeUserAsDefault(self, request: SetNativeUserAsDefaultRequest) -> SetNativeUserAsDefaultResponse:
		return self.stub.SetNativeUserAsDefault(request, metadata=self.headers)

	def CreateNativeUserIdentityLink(self, request: CreateNativeUserIdentityLinkRequest) -> CreateNativeUserIdentityLinkResponse:
		return self.stub.CreateNativeUserIdentityLink(request, metadata=self.headers)

	def CreateNativeUserIdentityLinkV2(self, request: CreateNativeUserIdentityLinkV2Request) -> CreateNativeUserIdentityLinkV2Response:
		return self.stub.CreateNativeUserIdentityLinkV2(request, metadata=self.headers)

	def GetNativeUserIdentityLink(self, request: GetNativeUserIdentityLinkRequest) -> GetNativeUserIdentityLinkResponse:
		return self.stub.GetNativeUserIdentityLink(request, metadata=self.headers)

	def DeleteNativeUserIdentityLink(self, request: DeleteNativeUserIdentityLinkRequest) -> DeleteNativeUserIdentityLinkResponse:
		return self.stub.DeleteNativeUserIdentityLink(request, metadata=self.headers)

