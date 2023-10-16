import grpc


from .gen.admin.v1.permissions_pb2 import (
	GetPermissionsByServiceRequest,
	GetPermissionsByServiceResponse,
	GetPermissionsRequest,
	GetPermissionsResponse,
)

from .gen.admin.v1.permissions_pb2_grpc import PermissionServiceStub
class PermissionService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = PermissionServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def GetPermissions(self, request: GetPermissionsRequest) -> GetPermissionsResponse:
		return self.stub.GetPermissions(request, metadata=self.headers)

	def GetPermissionsByService(self, request: GetPermissionsByServiceRequest) -> GetPermissionsByServiceResponse:
		return self.stub.GetPermissionsByService(request, metadata=self.headers)

