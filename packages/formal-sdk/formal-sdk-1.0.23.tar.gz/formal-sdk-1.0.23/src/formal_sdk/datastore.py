import grpc


from .gen.admin.v1.datastore_pb2 import (
	CreateDatastoreRequest,
	CreateDatastoreResponse,
	GetDatastoreRequest,
	GetDatastoreResponse,
	GetDatastoresRequest,
	GetDatastoresResponse,
	DeleteDatastoreRequest,
	DeleteDatastoreResponse,
	UpdateDatastoreNameRequest,
	UpdateDatastoreNameResponse,
	UpdateDbDiscoveryConfigRequest,
	UpdateDbDiscoveryConfigResponse,
	UpdateDataStoreHealthCheckDbNameRequest,
	UpdateDataStoreHealthCheckDbNameResponse,
	UpdateDataStoreDefaultAccessBehaviorRequest,
	UpdateDataStoreDefaultAccessBehaviorResponse,
	GetLinkedSidecarsRequest,
	GetLinkedSidecarsResponse,
	LinkedSidecar,
	Datastore,
	IntegrationLog,
)

from .gen.admin.v1.datastore_pb2_grpc import DataStoreServiceStub
class DataStoreService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = DataStoreServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def CreateDatastore(self, request: CreateDatastoreRequest) -> CreateDatastoreResponse:
		return self.stub.CreateDatastore(request, metadata=self.headers)

	def GetDatastore(self, request: GetDatastoreRequest) -> GetDatastoreResponse:
		return self.stub.GetDatastore(request, metadata=self.headers)

	def GetDatastores(self, request: GetDatastoresRequest) -> GetDatastoresResponse:
		return self.stub.GetDatastores(request, metadata=self.headers)

	def GetLinkedSidecars(self, request: GetLinkedSidecarsRequest) -> GetLinkedSidecarsResponse:
		return self.stub.GetLinkedSidecars(request, metadata=self.headers)

	def DeleteDatastore(self, request: DeleteDatastoreRequest) -> DeleteDatastoreResponse:
		return self.stub.DeleteDatastore(request, metadata=self.headers)

	def UpdateDatastoreName(self, request: UpdateDatastoreNameRequest) -> UpdateDatastoreNameResponse:
		return self.stub.UpdateDatastoreName(request, metadata=self.headers)

	def UpdateDbDiscoveryConfig(self, request: UpdateDbDiscoveryConfigRequest) -> UpdateDbDiscoveryConfigResponse:
		return self.stub.UpdateDbDiscoveryConfig(request, metadata=self.headers)

	def UpdateDataStoreHealthCheckDbName(self, request: UpdateDataStoreHealthCheckDbNameRequest) -> UpdateDataStoreHealthCheckDbNameResponse:
		return self.stub.UpdateDataStoreHealthCheckDbName(request, metadata=self.headers)

	def UpdateDataStoreDefaultAccessBehavior(self, request: UpdateDataStoreDefaultAccessBehaviorRequest) -> UpdateDataStoreDefaultAccessBehaviorResponse:
		return self.stub.UpdateDataStoreDefaultAccessBehavior(request, metadata=self.headers)

