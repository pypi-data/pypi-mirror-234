import grpc


from .gen.admin.v1.integration_github_pb2 import (
	InstallGithubAppRequest,
	InstallGithubAppResponse,
	GetGithubAppForOrgRequest,
	GetGithubAppForOrgResponse,
)

from .gen.admin.v1.integration_github_pb2_grpc import GithubServiceStub
class GithubService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = GithubServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def InstallGithubApp(self, request: InstallGithubAppRequest) -> InstallGithubAppResponse:
		return self.stub.InstallGithubApp(request, metadata=self.headers)

	def GetGithubAppForOrg(self, request: GetGithubAppForOrgRequest) -> GetGithubAppForOrgResponse:
		return self.stub.GetGithubAppForOrg(request, metadata=self.headers)

