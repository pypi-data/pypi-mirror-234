import grpc


from .gen.admin.v1.etl_pb2 import (
	GetGroupsRequest,
	GetGroupsResponse,
	GetConnectorsRequest,
	GetConnectorsResponse,
	GetConnectorByDbNameRequest,
	GetConnectorByDbNameResponse,
	GetDestinationsRequest,
	GetDestinationsResponse,
	GetDestinationByIDRequest,
	GetDestinationByIDResponse,
	GetLineageSchemasRequest,
	GetLineageSchemasResponse,
	GetLineageSchemaByNameRequest,
	GetLineageSchemaByNameResponse,
	GetLineageTablesRequest,
	GetLineageTablesResponse,
	GetLineageTableByNameRequest,
	GetLineageTableByNameResponse,
	GetLineageColumnsRequest,
	GetLineageColumnsResponse,
	GetLineageColumnsByTableRequest,
	GetLineageColumnsByTableResponse,
)

from .gen.admin.v1.etl_pb2_grpc import ETLServiceStub
class ETLService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = ETLServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def GetConnectors(self, request: GetConnectorsRequest) -> GetConnectorsResponse:
		return self.stub.GetConnectors(request, metadata=self.headers)

	def GetConnectorByDbName(self, request: GetConnectorByDbNameRequest) -> GetConnectorByDbNameResponse:
		return self.stub.GetConnectorByDbName(request, metadata=self.headers)

	def GetDestinations(self, request: GetDestinationsRequest) -> GetDestinationsResponse:
		return self.stub.GetDestinations(request, metadata=self.headers)

	def GetDestinationByID(self, request: GetDestinationByIDRequest) -> GetDestinationByIDResponse:
		return self.stub.GetDestinationByID(request, metadata=self.headers)

	def GetGroups(self, request: GetGroupsRequest) -> GetGroupsResponse:
		return self.stub.GetGroups(request, metadata=self.headers)

	def GetLineageSchemas(self, request: GetLineageSchemasRequest) -> GetLineageSchemasResponse:
		return self.stub.GetLineageSchemas(request, metadata=self.headers)

	def GetLineageSchemaByName(self, request: GetLineageSchemaByNameRequest) -> GetLineageSchemaByNameResponse:
		return self.stub.GetLineageSchemaByName(request, metadata=self.headers)

	def GetLineageTables(self, request: GetLineageTablesRequest) -> GetLineageTablesResponse:
		return self.stub.GetLineageTables(request, metadata=self.headers)

	def GetLineageTableByName(self, request: GetLineageTableByNameRequest) -> GetLineageTableByNameResponse:
		return self.stub.GetLineageTableByName(request, metadata=self.headers)

	def GetLineageColumns(self, request: GetLineageColumnsRequest) -> GetLineageColumnsResponse:
		return self.stub.GetLineageColumns(request, metadata=self.headers)

	def GetLineageColumnsByTable(self, request: GetLineageColumnsByTableRequest) -> GetLineageColumnsByTableResponse:
		return self.stub.GetLineageColumnsByTable(request, metadata=self.headers)

