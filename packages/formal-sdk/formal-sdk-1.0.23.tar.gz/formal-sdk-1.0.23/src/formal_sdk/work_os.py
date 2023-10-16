import grpc


from .gen.admin.v1.work_os_pb2 import (
	GetDirectoryRequest,
	GetDirectoryResponse,
	Directory,
	GetGroupsByDirectoryIdRequest,
	GetGroupsByDirectoryIdResponse,
	GetUsersByDirectoryIdRequest,
	GetUsersByDirectoryIdResponse,
	GetWorkOsGroupByIdRequest,
	GetWorkOsGroupByIdResponse,
	DirectorySyncGroup,
	UserEmail,
	UserGroup,
	WorkUser,
	Users,
	Group,
	GroupPair,
	GetDirectoryGroupsRequest,
	GetDirectoryGroupsResponse,
	UpdateDirectoryGroupSyncRequest,
	UpdateDirectoryGroupSyncResponse,
	GetDSyncPortalRequest,
	GetDSyncPortalResponse,
)

from .gen.admin.v1.work_os_pb2_grpc import DSyncServiceStub
class DSyncService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = DSyncServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def GetDirectory(self, request: GetDirectoryRequest) -> GetDirectoryResponse:
		return self.stub.GetDirectory(request, metadata=self.headers)

	def GetGroupsByDirectoryId(self, request: GetGroupsByDirectoryIdRequest) -> GetGroupsByDirectoryIdResponse:
		return self.stub.GetGroupsByDirectoryId(request, metadata=self.headers)

	def GetUsersByDirectoryId(self, request: GetUsersByDirectoryIdRequest) -> GetUsersByDirectoryIdResponse:
		return self.stub.GetUsersByDirectoryId(request, metadata=self.headers)

	def GetWorkOsGroupById(self, request: GetWorkOsGroupByIdRequest) -> GetWorkOsGroupByIdResponse:
		return self.stub.GetWorkOsGroupById(request, metadata=self.headers)

	def GetDirectoryGroups(self, request: GetDirectoryGroupsRequest) -> GetDirectoryGroupsResponse:
		return self.stub.GetDirectoryGroups(request, metadata=self.headers)

	def UpdateDirectoryGroupSync(self, request: UpdateDirectoryGroupSyncRequest) -> UpdateDirectoryGroupSyncResponse:
		return self.stub.UpdateDirectoryGroupSync(request, metadata=self.headers)

	def GetDSyncPortal(self, request: GetDSyncPortalRequest) -> GetDSyncPortalResponse:
		return self.stub.GetDSyncPortal(request, metadata=self.headers)

