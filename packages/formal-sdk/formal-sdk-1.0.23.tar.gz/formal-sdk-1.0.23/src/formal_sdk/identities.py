import grpc


from .gen.admin.v1.identities_pb2 import (
	ListGroupsRequest,
	CreateGroupRequest,
	GetGroupByIdRequest,
	DeleteGroupRequest,
	UpdateGroupRequest,
	LinkUsersToGroupRequest,
	LinkUsersToGroupV2Request,
	UnlinkUsersFromGroupRequest,
	CreateGroupResponse,
	GetGroupByIdResponse,
	DeleteGroupResponse,
	UpdateGroupResponse,
	ListGroupsResponse,
	LinkUsersToGroupResponse,
	LinkUsersToGroupV2Response,
	UnlinkUsersFromGroupResponse,
	UserLinkGroupResponse,
	ListUsersRequest,
	ListUsersResponse,
	CreateUserRequest,
	CreateUserResponse,
	CreateUserV2Request,
	CreateUserV2Response,
	GetUserByIdRequest,
	GetUserByIdResponse,
	DeleteUserRequest,
	DeleteUserResponse,
	UpdateUserRequest,
	UpdateUserResponse,
	GetMachineUserAuthTokenRequest,
	GetMachineUserAuthTokenResponse,
	RefreshMachineUserAuthTokenRequest,
	RefreshMachineUserAuthTokenResponse,
	GetUserExternalIdsRequest,
	GetUserExternalIdsResponse,
	MapUserToExternalIdRequest,
	MapUserToExternalIdResponse,
	DeleteExternalIdMappingRequest,
	DeleteExternalIdMappingResponse,
)

from .gen.admin.v1.identities_pb2_grpc import UserServiceStub
class UserService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = UserServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def ListUsers(self, request: ListUsersRequest) -> ListUsersResponse:
		return self.stub.ListUsers(request, metadata=self.headers)

	def CreateUser(self, request: CreateUserRequest) -> CreateUserResponse:
		return self.stub.CreateUser(request, metadata=self.headers)

	def CreateUserV2(self, request: CreateUserV2Request) -> CreateUserV2Response:
		return self.stub.CreateUserV2(request, metadata=self.headers)

	def GetUserById(self, request: GetUserByIdRequest) -> GetUserByIdResponse:
		return self.stub.GetUserById(request, metadata=self.headers)

	def DeleteUser(self, request: DeleteUserRequest) -> DeleteUserResponse:
		return self.stub.DeleteUser(request, metadata=self.headers)

	def UpdateUser(self, request: UpdateUserRequest) -> UpdateUserResponse:
		return self.stub.UpdateUser(request, metadata=self.headers)

	def GetMachineUserAuthToken(self, request: GetMachineUserAuthTokenRequest) -> GetMachineUserAuthTokenResponse:
		return self.stub.GetMachineUserAuthToken(request, metadata=self.headers)

	def RefreshMachineUserAuthToken(self, request: RefreshMachineUserAuthTokenRequest) -> RefreshMachineUserAuthTokenResponse:
		return self.stub.RefreshMachineUserAuthToken(request, metadata=self.headers)

	def GetUserExternalIds(self, request: GetUserExternalIdsRequest) -> GetUserExternalIdsResponse:
		return self.stub.GetUserExternalIds(request, metadata=self.headers)

	def MapUserToExternalId(self, request: MapUserToExternalIdRequest) -> MapUserToExternalIdResponse:
		return self.stub.MapUserToExternalId(request, metadata=self.headers)

	def DeleteExternalIdMapping(self, request: DeleteExternalIdMappingRequest) -> DeleteExternalIdMappingResponse:
		return self.stub.DeleteExternalIdMapping(request, metadata=self.headers)

from .gen.admin.v1.identities_pb2_grpc import GroupServiceStub
class GroupService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = GroupServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def CreateGroup(self, request: CreateGroupRequest) -> CreateGroupResponse:
		return self.stub.CreateGroup(request, metadata=self.headers)

	def ListGroups(self, request: ListGroupsRequest) -> ListGroupsResponse:
		return self.stub.ListGroups(request, metadata=self.headers)

	def GetGroupById(self, request: GetGroupByIdRequest) -> GetGroupByIdResponse:
		return self.stub.GetGroupById(request, metadata=self.headers)

	def UpdateGroup(self, request: UpdateGroupRequest) -> UpdateGroupResponse:
		return self.stub.UpdateGroup(request, metadata=self.headers)

	def LinkUsersToGroup(self, request: LinkUsersToGroupRequest) -> LinkUsersToGroupResponse:
		return self.stub.LinkUsersToGroup(request, metadata=self.headers)

	def LinkUsersToGroupV2(self, request: LinkUsersToGroupV2Request) -> LinkUsersToGroupV2Response:
		return self.stub.LinkUsersToGroupV2(request, metadata=self.headers)

	def UnlinkUsersFromGroup(self, request: UnlinkUsersFromGroupRequest) -> UnlinkUsersFromGroupResponse:
		return self.stub.UnlinkUsersFromGroup(request, metadata=self.headers)

	def DeleteGroup(self, request: DeleteGroupRequest) -> DeleteGroupResponse:
		return self.stub.DeleteGroup(request, metadata=self.headers)

