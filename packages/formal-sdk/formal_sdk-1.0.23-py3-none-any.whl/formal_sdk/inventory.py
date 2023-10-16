import grpc


from .gen.admin.v1.inventory_pb2 import (
	GetInventoryFlatOldRequest,
	ColumnOld,
	GetInventoryFlatOldResponse,
	UpdateColumnFieldEncryptionRequest,
	UpdateColumnFieldEncryptionResponse,
	GetInventoryObjectRequest,
	GetInventoryObjectResponse,
	GetInventoryHierarchicalRequest,
	GetInventoryHierarchicalResponse,
	GetInventoryRequest,
	GetInventoryResponse,
	GetInventoryFlatRequest,
	Column,
	Ds,
	Db,
	Schema,
	Table,
	SubColumn,
	InventoryObject,
	GetInventoryFlatResponse,
	UpdateColumnLockStatusRequest,
	UpdateColumnLockStatusResponse,
	UpdateColumnDataLabelRequest,
	UpdateColumnDataLabelResponse,
	CreateInventoryObjectRequest,
	CreateInventoryObjectResponse,
	DeleteInventoryObjectRequest,
	DeleteInventoryObjectResponse,
	Tag,
	CreateInventoryTagRequest,
	CreateInventoryTagResponse,
	GetInventoryTagsRequest,
	GetInventoryTagsResponse,
	UpdateInventoryObjectTagsRequest,
	UpdateInventoryObjectTagsResponse,
	DeleteInventoryTagRequest,
	DeleteInventoryTagResponse,
	GetInventoryMetricsRequest,
	GetInventoryMetricsResponse,
	CreateDataDomainRequest,
	CreateDataDomainResponse,
	GetDataDomainsRequest,
	GetDataDomainsResponse,
	GetDataDomainByIdRequest,
	GetDataDomainByIdResponse,
	UpdateDataDomainRequest,
	UpdateDataDomainResponse,
	DeleteDataDomainRequest,
	DeleteDataDomainResponse,
)

from .gen.admin.v1.inventory_pb2_grpc import InventoryServiceStub
class InventoryService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = InventoryServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def GetInventoryHierarchical(self, request: GetInventoryHierarchicalRequest) -> GetInventoryHierarchicalResponse:
		return self.stub.GetInventoryHierarchical(request, metadata=self.headers)

	def GetInventory(self, request: GetInventoryRequest) -> GetInventoryResponse:
		return self.stub.GetInventory(request, metadata=self.headers)

	def GetInventoryFlat(self, request: GetInventoryFlatRequest) -> GetInventoryFlatResponse:
		return self.stub.GetInventoryFlat(request, metadata=self.headers)

	def GetInventoryFlatOld(self, request: GetInventoryFlatOldRequest) -> GetInventoryFlatOldResponse:
		return self.stub.GetInventoryFlatOld(request, metadata=self.headers)

	def GetInventoryObject(self, request: GetInventoryObjectRequest) -> GetInventoryObjectResponse:
		return self.stub.GetInventoryObject(request, metadata=self.headers)

	def UpdateColumnLockStatus(self, request: UpdateColumnLockStatusRequest) -> UpdateColumnLockStatusResponse:
		return self.stub.UpdateColumnLockStatus(request, metadata=self.headers)

	def UpdateColumnDataLabel(self, request: UpdateColumnDataLabelRequest) -> UpdateColumnDataLabelResponse:
		return self.stub.UpdateColumnDataLabel(request, metadata=self.headers)

	def UpdateColumnFieldEncryption(self, request: UpdateColumnFieldEncryptionRequest) -> UpdateColumnFieldEncryptionResponse:
		return self.stub.UpdateColumnFieldEncryption(request, metadata=self.headers)

	def UpdateInventoryObjectTags(self, request: UpdateInventoryObjectTagsRequest) -> UpdateInventoryObjectTagsResponse:
		return self.stub.UpdateInventoryObjectTags(request, metadata=self.headers)

	def CreateInventoryObject(self, request: CreateInventoryObjectRequest) -> CreateInventoryObjectResponse:
		return self.stub.CreateInventoryObject(request, metadata=self.headers)

	def DeleteInventoryObject(self, request: DeleteInventoryObjectRequest) -> DeleteInventoryObjectResponse:
		return self.stub.DeleteInventoryObject(request, metadata=self.headers)

	def CreateInventoryTag(self, request: CreateInventoryTagRequest) -> CreateInventoryTagResponse:
		return self.stub.CreateInventoryTag(request, metadata=self.headers)

	def GetInventoryTags(self, request: GetInventoryTagsRequest) -> GetInventoryTagsResponse:
		return self.stub.GetInventoryTags(request, metadata=self.headers)

	def DeleteInventoryTag(self, request: DeleteInventoryTagRequest) -> DeleteInventoryTagResponse:
		return self.stub.DeleteInventoryTag(request, metadata=self.headers)

	def GetInventoryMetrics(self, request: GetInventoryMetricsRequest) -> GetInventoryMetricsResponse:
		return self.stub.GetInventoryMetrics(request, metadata=self.headers)

	def CreateDataDomain(self, request: CreateDataDomainRequest) -> CreateDataDomainResponse:
		return self.stub.CreateDataDomain(request, metadata=self.headers)

	def GetDataDomains(self, request: GetDataDomainsRequest) -> GetDataDomainsResponse:
		return self.stub.GetDataDomains(request, metadata=self.headers)

	def GetDataDomainById(self, request: GetDataDomainByIdRequest) -> GetDataDomainByIdResponse:
		return self.stub.GetDataDomainById(request, metadata=self.headers)

	def UpdateDataDomain(self, request: UpdateDataDomainRequest) -> UpdateDataDomainResponse:
		return self.stub.UpdateDataDomain(request, metadata=self.headers)

	def DeleteDataDomain(self, request: DeleteDataDomainRequest) -> DeleteDataDomainResponse:
		return self.stub.DeleteDataDomain(request, metadata=self.headers)

