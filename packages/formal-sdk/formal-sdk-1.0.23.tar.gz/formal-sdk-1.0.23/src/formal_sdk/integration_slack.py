import grpc


from .gen.admin.v1.integration_slack_pb2 import (
	CreateSlackIntegrationRequest,
	CreateSlackIntegrationResponse,
	GetSlackIntegrationRequest,
	GetSlackIntegrationResponse,
)

from .gen.admin.v1.integration_slack_pb2_grpc import SlackServiceStub
class SlackService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = SlackServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def CreateSlackIntegration(self, request: CreateSlackIntegrationRequest) -> CreateSlackIntegrationResponse:
		return self.stub.CreateSlackIntegration(request, metadata=self.headers)

	def GetSlackIntegration(self, request: GetSlackIntegrationRequest) -> GetSlackIntegrationResponse:
		return self.stub.GetSlackIntegration(request, metadata=self.headers)

