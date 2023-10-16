import grpc


from .gen.admin.v1.metrics_pb2 import (
	GetMetricsRequest,
	Metric,
	Node,
	Link,
	GetMetricsResponse,
	RowLevelMetric,
	RowLevelMetricConfiguration,
	GetCustomMetricsDetailsRequest,
	GetCustomMetricsDetailsResponse,
	MetricsGroup,
	GetCustomMetricsRequest,
	GetCustomMetricsResponse,
	CreateCustomMetricRequest,
	CreateCustomMetricResponse,
	DeleteCustomMetricRequest,
	DeleteCustomMetricResponse,
)

from .gen.admin.v1.metrics_pb2_grpc import MetricsServiceStub
class MetricsService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = MetricsServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def GetMetrics(self, request: GetMetricsRequest) -> GetMetricsResponse:
		return self.stub.GetMetrics(request, metadata=self.headers)

	def CreateCustomMetric(self, request: CreateCustomMetricRequest) -> CreateCustomMetricResponse:
		return self.stub.CreateCustomMetric(request, metadata=self.headers)

	def GetCustomMetrics(self, request: GetCustomMetricsRequest) -> GetCustomMetricsResponse:
		return self.stub.GetCustomMetrics(request, metadata=self.headers)

	def GetCustomMetricsDetails(self, request: GetCustomMetricsDetailsRequest) -> GetCustomMetricsDetailsResponse:
		return self.stub.GetCustomMetricsDetails(request, metadata=self.headers)

	def DeleteCustomMetric(self, request: DeleteCustomMetricRequest) -> DeleteCustomMetricResponse:
		return self.stub.DeleteCustomMetric(request, metadata=self.headers)

