import grpc


from .gen.admin.v1.policies_pb2 import (
	PolicyRuleType,
	PolicyType,
	CreatePolicySuggestionRequest,
	CreatePolicySuggestionResponse,
	DeletePolicyRequest,
	DeletePolicyResponse,
	EvaluatePolicyValidityRequest,
	EvaluatePolicyValidityResponse,
	DryRunPoliciesRequest,
	ColumnPolicy,
	AWSAccount,
	AWSEC2,
	AWSECS,
	AWS,
	DryRunPoliciesResponse,
	CreatePolicyRequest,
	CreatePolicyV2Request,
	CreatePolicyResponse,
	CreatePolicyV2Response,
	UpdatePolicyRequest,
	UpdatePolicyV2Request,
	UpdatePolicyResponse,
	UpdatePolicyV2Response,
	GetPolicyRequest,
	GetPolicyV2Request,
	GetPolicyResponse,
	GetPolicyV2Response,
	GetPoliciesRequest,
	GetPoliciesResponse,
)

from .gen.admin.v1.policies_pb2_grpc import PolicyServiceStub
class PolicyService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = PolicyServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def GetPolicies(self, request: GetPoliciesRequest) -> GetPoliciesResponse:
		return self.stub.GetPolicies(request, metadata=self.headers)

	def GetPolicy(self, request: GetPolicyRequest) -> GetPolicyResponse:
		return self.stub.GetPolicy(request, metadata=self.headers)

	def GetPolicyV2(self, request: GetPolicyV2Request) -> GetPolicyV2Response:
		return self.stub.GetPolicyV2(request, metadata=self.headers)

	def CreatePolicy(self, request: CreatePolicyRequest) -> CreatePolicyResponse:
		return self.stub.CreatePolicy(request, metadata=self.headers)

	def CreatePolicyV2(self, request: CreatePolicyV2Request) -> CreatePolicyV2Response:
		return self.stub.CreatePolicyV2(request, metadata=self.headers)

	def UpdatePolicy(self, request: UpdatePolicyRequest) -> UpdatePolicyResponse:
		return self.stub.UpdatePolicy(request, metadata=self.headers)

	def UpdatePolicyV2(self, request: UpdatePolicyV2Request) -> UpdatePolicyV2Response:
		return self.stub.UpdatePolicyV2(request, metadata=self.headers)

	def DeletePolicy(self, request: DeletePolicyRequest) -> DeletePolicyResponse:
		return self.stub.DeletePolicy(request, metadata=self.headers)

	def DryRunPolicies(self, request: DryRunPoliciesRequest) -> DryRunPoliciesResponse:
		return self.stub.DryRunPolicies(request, metadata=self.headers)

	def EvaluatePolicyValidity(self, request: EvaluatePolicyValidityRequest) -> EvaluatePolicyValidityResponse:
		return self.stub.EvaluatePolicyValidity(request, metadata=self.headers)

	def CreatePolicySuggestion(self, request: CreatePolicySuggestionRequest) -> CreatePolicySuggestionResponse:
		return self.stub.CreatePolicySuggestion(request, metadata=self.headers)

