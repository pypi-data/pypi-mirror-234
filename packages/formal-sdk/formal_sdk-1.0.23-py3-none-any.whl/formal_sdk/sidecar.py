import grpc


from .gen.admin.v1.sidecar_pb2 import (
	ListSidecarsRequest,
	ListSidecarsResponse,
	GetSidecarVersionsRequest,
	GetSidecarVersionsResponse,
	CreateSidecarRequest,
	CreateSidecarResponse,
	GetSidecarByIdRequest,
	GetSidecarByIdResponse,
	GetSidecarTlsCertificateByIdRequest,
	GetSidecarTlsCertificateByIdResponse,
	UpdateSidecarNameRequest,
	UpdateSidecarNameResponse,
	UpdateSidecarVersionRequest,
	UpdateSidecarVersionResponse,
	UpdateSidecarFormalHostnameRequest,
	UpdateSidecarFormalHostnameResponse,
	UpdateSidecarKmsDecryptPolicyRequest,
	UpdateSidecarKmsDecryptPolicyResponse,
	DeleteSidecarRequest,
	DeleteSidecarResponse,
	CreateSidecarDatastoreLinkRequest,
	CreateSidecarDatastoreLinkResponse,
	DeleteSidecarDatastoreLinkRequest,
	DeleteSidecarDatastoreLinkResponse,
	GetLinkByIdRequest,
	GetLinkByIdResponse,
	GetLinksBySidecarIdRequest,
	GetLinksBySidecarIdResponse,
	GetLinksByDatastoreIdRequest,
	GetLinksByDatastoreIdResponse,
)

from .gen.admin.v1.sidecar_pb2_grpc import SidecarServiceStub
class SidecarService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = SidecarServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def ListSidecars(self, request: ListSidecarsRequest) -> ListSidecarsResponse:
		return self.stub.ListSidecars(request, metadata=self.headers)

	def GetSidecarVersions(self, request: GetSidecarVersionsRequest) -> GetSidecarVersionsResponse:
		return self.stub.GetSidecarVersions(request, metadata=self.headers)

	def CreateSidecar(self, request: CreateSidecarRequest) -> CreateSidecarResponse:
		return self.stub.CreateSidecar(request, metadata=self.headers)

	def GetSidecarById(self, request: GetSidecarByIdRequest) -> GetSidecarByIdResponse:
		return self.stub.GetSidecarById(request, metadata=self.headers)

	def GetSidecarTlsCertificateById(self, request: GetSidecarTlsCertificateByIdRequest) -> GetSidecarTlsCertificateByIdResponse:
		return self.stub.GetSidecarTlsCertificateById(request, metadata=self.headers)

	def UpdateSidecarName(self, request: UpdateSidecarNameRequest) -> UpdateSidecarNameResponse:
		return self.stub.UpdateSidecarName(request, metadata=self.headers)

	def UpdateSidecarVersion(self, request: UpdateSidecarVersionRequest) -> UpdateSidecarVersionResponse:
		return self.stub.UpdateSidecarVersion(request, metadata=self.headers)

	def UpdateSidecarFormalHostname(self, request: UpdateSidecarFormalHostnameRequest) -> UpdateSidecarFormalHostnameResponse:
		return self.stub.UpdateSidecarFormalHostname(request, metadata=self.headers)

	def UpdateSidecarKmsDecryptPolicy(self, request: UpdateSidecarKmsDecryptPolicyRequest) -> UpdateSidecarKmsDecryptPolicyResponse:
		return self.stub.UpdateSidecarKmsDecryptPolicy(request, metadata=self.headers)

	def DeleteSidecar(self, request: DeleteSidecarRequest) -> DeleteSidecarResponse:
		return self.stub.DeleteSidecar(request, metadata=self.headers)

	def CreateSidecarDatastoreLink(self, request: CreateSidecarDatastoreLinkRequest) -> CreateSidecarDatastoreLinkResponse:
		return self.stub.CreateSidecarDatastoreLink(request, metadata=self.headers)

	def GetLinkById(self, request: GetLinkByIdRequest) -> GetLinkByIdResponse:
		return self.stub.GetLinkById(request, metadata=self.headers)

	def GetLinksBySidecarId(self, request: GetLinksBySidecarIdRequest) -> GetLinksBySidecarIdResponse:
		return self.stub.GetLinksBySidecarId(request, metadata=self.headers)

	def GetLinksByDatastoreId(self, request: GetLinksByDatastoreIdRequest) -> GetLinksByDatastoreIdResponse:
		return self.stub.GetLinksByDatastoreId(request, metadata=self.headers)

	def DeleteSidecarDatastoreLink(self, request: DeleteSidecarDatastoreLinkRequest) -> DeleteSidecarDatastoreLinkResponse:
		return self.stub.DeleteSidecarDatastoreLink(request, metadata=self.headers)

