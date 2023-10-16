import grpc


from .gen.admin.v1.search_pb2 import (
	SearchRequest,
	SearchResponse,
	WrappedSearchUser,
	WrappedSearchGroup,
	WrappedSearchPolicy,
	WrappedSearchDatastore,
	WrappedSearchSidecar,
	WrappedSearchInventory,
)

from .gen.admin.v1.search_pb2_grpc import SearchServiceStub
class SearchService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = SearchServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def Search(self, request: SearchRequest) -> SearchResponse:
		return self.stub.Search(request, metadata=self.headers)

