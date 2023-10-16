import grpc


from .gen.admin.v1.cord_pb2 import (
	GetClientAuthTokenRequest,
	GetClientAuthTokenResponse,
)

from .gen.admin.v1.cord_pb2_grpc import CordServiceStub
class CordService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = CordServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def GetClientAuthToken(self, request: GetClientAuthTokenRequest) -> GetClientAuthTokenResponse:
		return self.stub.GetClientAuthToken(request, metadata=self.headers)

