from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FlatDataplane(_message.Message):
    __slots__ = ["id", "name", "region", "customer_vpc_id", "original_customer_vpc_id", "cloud_account_id", "availability_zone", "vpc_peering_connection_id", "formal_r53_private_hosted_zone_id", "formal_vpc_flow_logs_group_arn", "formal_vpc_flow_log_group_name", "formal_vpc_flow_logs_iam_role_arn", "formal_vpc_flow_logs_iam_policy_arn", "formal_vpc_igw_id", "egress_only_igw", "formal_vpc_private_subnets_ids", "formal_vpc_public_subnets_ids", "formal_public_subnets", "formal_private_subnets", "formal_vpc_public_route_table_id", "customer_vpc_route_tables", "formal_vpc_natg_ids", "formal_vpc_natg_eips", "formal_vpc_public_route_tables", "formal_vpc_private_route_table_routes", "formal_vpc_id", "formal_vpc_cidr_block", "ecs_cluster_name", "ecs_cluster_arn", "status", "vpc_peering"]
    class FormalVpcPrivateSubnetsIdsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class FormalVpcPublicSubnetsIdsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class FormalVpcNatgIdsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class FormalVpcNatgEipsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_VPC_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_CUSTOMER_VPC_ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    AVAILABILITY_ZONE_FIELD_NUMBER: _ClassVar[int]
    VPC_PEERING_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    FORMAL_R53_PRIVATE_HOSTED_ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    FORMAL_VPC_FLOW_LOGS_GROUP_ARN_FIELD_NUMBER: _ClassVar[int]
    FORMAL_VPC_FLOW_LOG_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    FORMAL_VPC_FLOW_LOGS_IAM_ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    FORMAL_VPC_FLOW_LOGS_IAM_POLICY_ARN_FIELD_NUMBER: _ClassVar[int]
    FORMAL_VPC_IGW_ID_FIELD_NUMBER: _ClassVar[int]
    EGRESS_ONLY_IGW_FIELD_NUMBER: _ClassVar[int]
    FORMAL_VPC_PRIVATE_SUBNETS_IDS_FIELD_NUMBER: _ClassVar[int]
    FORMAL_VPC_PUBLIC_SUBNETS_IDS_FIELD_NUMBER: _ClassVar[int]
    FORMAL_PUBLIC_SUBNETS_FIELD_NUMBER: _ClassVar[int]
    FORMAL_PRIVATE_SUBNETS_FIELD_NUMBER: _ClassVar[int]
    FORMAL_VPC_PUBLIC_ROUTE_TABLE_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_VPC_ROUTE_TABLES_FIELD_NUMBER: _ClassVar[int]
    FORMAL_VPC_NATG_IDS_FIELD_NUMBER: _ClassVar[int]
    FORMAL_VPC_NATG_EIPS_FIELD_NUMBER: _ClassVar[int]
    FORMAL_VPC_PUBLIC_ROUTE_TABLES_FIELD_NUMBER: _ClassVar[int]
    FORMAL_VPC_PRIVATE_ROUTE_TABLE_ROUTES_FIELD_NUMBER: _ClassVar[int]
    FORMAL_VPC_ID_FIELD_NUMBER: _ClassVar[int]
    FORMAL_VPC_CIDR_BLOCK_FIELD_NUMBER: _ClassVar[int]
    ECS_CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    ECS_CLUSTER_ARN_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VPC_PEERING_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    region: str
    customer_vpc_id: str
    original_customer_vpc_id: str
    cloud_account_id: str
    availability_zone: int
    vpc_peering_connection_id: str
    formal_r53_private_hosted_zone_id: str
    formal_vpc_flow_logs_group_arn: str
    formal_vpc_flow_log_group_name: str
    formal_vpc_flow_logs_iam_role_arn: str
    formal_vpc_flow_logs_iam_policy_arn: str
    formal_vpc_igw_id: str
    egress_only_igw: str
    formal_vpc_private_subnets_ids: _containers.ScalarMap[str, str]
    formal_vpc_public_subnets_ids: _containers.ScalarMap[str, str]
    formal_public_subnets: _containers.RepeatedScalarFieldContainer[str]
    formal_private_subnets: _containers.RepeatedScalarFieldContainer[str]
    formal_vpc_public_route_table_id: str
    customer_vpc_route_tables: _containers.RepeatedScalarFieldContainer[str]
    formal_vpc_natg_ids: _containers.ScalarMap[str, str]
    formal_vpc_natg_eips: _containers.ScalarMap[str, str]
    formal_vpc_public_route_tables: str
    formal_vpc_private_route_table_routes: _containers.RepeatedScalarFieldContainer[str]
    formal_vpc_id: str
    formal_vpc_cidr_block: str
    ecs_cluster_name: str
    ecs_cluster_arn: str
    status: str
    vpc_peering: bool
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., region: _Optional[str] = ..., customer_vpc_id: _Optional[str] = ..., original_customer_vpc_id: _Optional[str] = ..., cloud_account_id: _Optional[str] = ..., availability_zone: _Optional[int] = ..., vpc_peering_connection_id: _Optional[str] = ..., formal_r53_private_hosted_zone_id: _Optional[str] = ..., formal_vpc_flow_logs_group_arn: _Optional[str] = ..., formal_vpc_flow_log_group_name: _Optional[str] = ..., formal_vpc_flow_logs_iam_role_arn: _Optional[str] = ..., formal_vpc_flow_logs_iam_policy_arn: _Optional[str] = ..., formal_vpc_igw_id: _Optional[str] = ..., egress_only_igw: _Optional[str] = ..., formal_vpc_private_subnets_ids: _Optional[_Mapping[str, str]] = ..., formal_vpc_public_subnets_ids: _Optional[_Mapping[str, str]] = ..., formal_public_subnets: _Optional[_Iterable[str]] = ..., formal_private_subnets: _Optional[_Iterable[str]] = ..., formal_vpc_public_route_table_id: _Optional[str] = ..., customer_vpc_route_tables: _Optional[_Iterable[str]] = ..., formal_vpc_natg_ids: _Optional[_Mapping[str, str]] = ..., formal_vpc_natg_eips: _Optional[_Mapping[str, str]] = ..., formal_vpc_public_route_tables: _Optional[str] = ..., formal_vpc_private_route_table_routes: _Optional[_Iterable[str]] = ..., formal_vpc_id: _Optional[str] = ..., formal_vpc_cidr_block: _Optional[str] = ..., ecs_cluster_name: _Optional[str] = ..., ecs_cluster_arn: _Optional[str] = ..., status: _Optional[str] = ..., vpc_peering: bool = ...) -> None: ...

class DataplaneTransitGatewayRoutes(_message.Message):
    __slots__ = ["id", "dataplane_id", "destination_cidr_block", "transit_gateway_id", "vpc_peering_connection_id", "deployed"]
    ID_FIELD_NUMBER: _ClassVar[int]
    DATAPLANE_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_CIDR_BLOCK_FIELD_NUMBER: _ClassVar[int]
    TRANSIT_GATEWAY_ID_FIELD_NUMBER: _ClassVar[int]
    VPC_PEERING_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYED_FIELD_NUMBER: _ClassVar[int]
    id: str
    dataplane_id: str
    destination_cidr_block: str
    transit_gateway_id: str
    vpc_peering_connection_id: str
    deployed: bool
    def __init__(self, id: _Optional[str] = ..., dataplane_id: _Optional[str] = ..., destination_cidr_block: _Optional[str] = ..., transit_gateway_id: _Optional[str] = ..., vpc_peering_connection_id: _Optional[str] = ..., deployed: bool = ...) -> None: ...

class CloudIntegration(_message.Message):
    __slots__ = ["id", "aws_formal_id", "cloud_account_name", "url", "cloud_provider", "aws_account_id", "aws_formal_iam_role", "aws_formal_handshake_id", "gcp_project_id", "template_body", "aws_formal_user_name", "aws_formal_pingback_arn", "aws_formal_stack_name", "aws_cloud_region", "aws_formal_r53_private_hosted_zone_id", "stacks", "created_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    AWS_FORMAL_ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_ACCOUNT_NAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    CLOUD_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    AWS_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    AWS_FORMAL_IAM_ROLE_FIELD_NUMBER: _ClassVar[int]
    AWS_FORMAL_HANDSHAKE_ID_FIELD_NUMBER: _ClassVar[int]
    GCP_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_BODY_FIELD_NUMBER: _ClassVar[int]
    AWS_FORMAL_USER_NAME_FIELD_NUMBER: _ClassVar[int]
    AWS_FORMAL_PINGBACK_ARN_FIELD_NUMBER: _ClassVar[int]
    AWS_FORMAL_STACK_NAME_FIELD_NUMBER: _ClassVar[int]
    AWS_CLOUD_REGION_FIELD_NUMBER: _ClassVar[int]
    AWS_FORMAL_R53_PRIVATE_HOSTED_ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    STACKS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    aws_formal_id: str
    cloud_account_name: str
    url: str
    cloud_provider: str
    aws_account_id: str
    aws_formal_iam_role: str
    aws_formal_handshake_id: str
    gcp_project_id: str
    template_body: str
    aws_formal_user_name: str
    aws_formal_pingback_arn: str
    aws_formal_stack_name: str
    aws_cloud_region: str
    aws_formal_r53_private_hosted_zone_id: str
    stacks: _containers.RepeatedCompositeFieldContainer[FlatDataplane]
    created_at: str
    def __init__(self, id: _Optional[str] = ..., aws_formal_id: _Optional[str] = ..., cloud_account_name: _Optional[str] = ..., url: _Optional[str] = ..., cloud_provider: _Optional[str] = ..., aws_account_id: _Optional[str] = ..., aws_formal_iam_role: _Optional[str] = ..., aws_formal_handshake_id: _Optional[str] = ..., gcp_project_id: _Optional[str] = ..., template_body: _Optional[str] = ..., aws_formal_user_name: _Optional[str] = ..., aws_formal_pingback_arn: _Optional[str] = ..., aws_formal_stack_name: _Optional[str] = ..., aws_cloud_region: _Optional[str] = ..., aws_formal_r53_private_hosted_zone_id: _Optional[str] = ..., stacks: _Optional[_Iterable[_Union[FlatDataplane, _Mapping]]] = ..., created_at: _Optional[str] = ...) -> None: ...
