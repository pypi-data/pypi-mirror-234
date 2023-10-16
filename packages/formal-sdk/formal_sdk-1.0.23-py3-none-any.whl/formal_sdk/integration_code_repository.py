import grpc


from .gen.admin.v1.integration_code_repository_pb2 import (
	DeleteCodeRepoByIdRequest,
	DeleteCodeRepoByIdResponse,
	CancelDeleteCodeRepoByIdRequest,
	CancelDeleteCodeRepoByIdResponse,
	ConnectCodeRepositoryRequest,
	ConnectCodeRepositoryResponse,
	GetAccessTokenRequest,
	GetAccessTokenResponse,
	GetGithubRepositoriesFromAuthUserRequest,
	GetGithubRepositoriesFromAuthUserResponse,
	GetUserAccessTokenRequest,
	GetUserAccessTokenResponse,
	GetCodeReposRequest,
	GetCodeReposResponse,
	CreateCodeRepoRequest,
	CreateCodeRepoResponse,
)

from .gen.admin.v1.integration_code_repository_pb2_grpc import CodeRepositoryServiceStub
class CodeRepositoryService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = CodeRepositoryServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def DeleteCodeRepoById(self, request: DeleteCodeRepoByIdRequest) -> DeleteCodeRepoByIdResponse:
		return self.stub.DeleteCodeRepoById(request, metadata=self.headers)

	def CancelDeleteCodeRepoById(self, request: CancelDeleteCodeRepoByIdRequest) -> CancelDeleteCodeRepoByIdResponse:
		return self.stub.CancelDeleteCodeRepoById(request, metadata=self.headers)

	def ConnectCodeRepository(self, request: ConnectCodeRepositoryRequest) -> ConnectCodeRepositoryResponse:
		return self.stub.ConnectCodeRepository(request, metadata=self.headers)

	def GetAccessToken(self, request: GetAccessTokenRequest) -> GetAccessTokenResponse:
		return self.stub.GetAccessToken(request, metadata=self.headers)

	def GetGithubRepositoriesFromAuthUser(self, request: GetGithubRepositoriesFromAuthUserRequest) -> GetGithubRepositoriesFromAuthUserResponse:
		return self.stub.GetGithubRepositoriesFromAuthUser(request, metadata=self.headers)

	def GetUserAccessToken(self, request: GetUserAccessTokenRequest) -> GetUserAccessTokenResponse:
		return self.stub.GetUserAccessToken(request, metadata=self.headers)

	def GetCodeRepos(self, request: GetCodeReposRequest) -> GetCodeReposResponse:
		return self.stub.GetCodeRepos(request, metadata=self.headers)

	def CreateCodeRepo(self, request: CreateCodeRepoRequest) -> CreateCodeRepoResponse:
		return self.stub.CreateCodeRepo(request, metadata=self.headers)

