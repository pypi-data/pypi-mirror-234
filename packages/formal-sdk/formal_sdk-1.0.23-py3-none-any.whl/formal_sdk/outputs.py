import grpc


from .gen.admin.v1.outputs_pb2 import (
	GetOutputsRequest,
	GetOutputsResponse,
	OutputRecord,
)

from .gen.admin.v1.outputs_pb2_grpc import OutputsServiceStub
class OutputsService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = OutputsServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def GetOutputs(self, request: GetOutputsRequest) -> GetOutputsResponse:
		return self.stub.GetOutputs(request, metadata=self.headers)

