from typing import List, Dict, Optional, Any, Union
from uuid import UUID
from datetime import date

import pydantic
from pydantic import Field

from bodosdk.models.base import ClusterStatus, CamelCaseBase, PageMetadata


class InstanceType(CamelCaseBase):
    name: str
    vcpus: int
    cores: int
    memory: int
    efa: Optional[bool] = None
    accelerated_networking: Optional[bool] = Field(None, alias="acceleratedNetworking")


class InstanceCategory(pydantic.BaseModel):
    name: str
    instance_types: Dict[str, InstanceType]


class BodoImage(pydantic.BaseModel):
    image_id: str
    bodo_version: str


class ClusterMetadata(pydantic.BaseModel):
    name: str
    uuid: str
    status: ClusterStatus
    description: str


class ClusterDefinition(CamelCaseBase):
    name: str
    instance_type: str = Field(..., alias="instanceType")
    workers_quantity: int = Field(..., alias="workersQuantity")
    auto_stop: Optional[int] = Field(None, alias="autoStop")  # in minutes
    auto_pause: Optional[int] = Field(None, alias="autoPause")  # in minutes
    image_id: Optional[str] = Field(None, alias="imageId")
    bodo_version: str = Field(..., alias="bodoVersion")
    description: Optional[str] = None
    accelerated_networking: Optional[bool] = Field(False, alias="acceleratedNetworking")
    is_job_dedicated: Optional[bool] = Field(False, alias="isJobDedicated")
    availability_zone: Optional[str] = Field(None, alias="availabilityZone")
    aws_deployment_subnet_id: Optional[str] = Field(None, alias="awsDeploymentSubnetId")
    instance_role_uuid: Optional[str] = Field(None, alias="instanceRoleUUID")
    auto_az: Optional[bool] = Field(True, alias="autoAZ")
    use_spot_instance: Optional[bool] = Field(False, alias="useSpotInstance")

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.use_spot_instance:
            self.auto_pause = 0 if self.auto_pause is None else self.auto_pause
            self.auto_stop = 60 if self.auto_stop is None else self.auto_stop
        else:
            self.auto_pause = 60 if self.auto_pause is None else self.auto_pause
            self.auto_stop = 0 if self.auto_stop is None else self.auto_stop


class ClusterResponse(CamelCaseBase):
    name: str
    uuid: Union[str, UUID]
    status: ClusterStatus
    description: Optional[str] = ""
    instance_type: str = Field(..., alias="instanceType")
    workers_quantity: int = Field(..., alias="workersQuantity")
    auto_stop: Optional[int] = Field(None, alias="autoStop")
    auto_pause: Optional[int] = Field(None, alias="autoPause")
    nodes_ip: Optional[List[str]] = Field(None, alias="nodesIp")
    bodo_version: Optional[str] = Field(None, alias="bodoVersion")
    image_id: str = Field(..., alias="imageId")
    cores_per_worker: Optional[int] = Field(None, alias="coresPerWorker")
    accelerated_networking: bool = Field(..., alias="acceleratedNetworking")
    autoscaling_identifier: Optional[str] = Field(None, alias="autoscalingIdentifier")
    last_asg_activity_id: Optional[str] = Field(None, alias="lastAsgActivityId")
    created_at: str = Field(..., alias="createdAt")
    is_job_dedicated: bool = Field(..., alias="isJobDedicated")
    last_known_activity: Optional[str] = Field(None, alias="lastKnownActivity")
    aws_deployment_subnet_id: Optional[str] = Field(None, alias="awsDeploymentSubnetId")
    node_metadata: Optional[object] = Field(None, alias="nodeMetadata")
    asg_metadata: Optional[object] = Field(None, alias="asgMetadata")
    auto_az: Optional[bool] = Field(True, alias="autoAZ")
    use_spot_instance: Optional[bool] = Field(False, alias="useSpotInstance")
    workspace: Any


class ScaleCluster(CamelCaseBase):
    uuid: Union[str, UUID]
    workers_quantity: int = Field(..., alias="workersQuantity")


class ModifyCluster(CamelCaseBase):
    uuid: Union[str, UUID]
    auto_stop: Optional[int] = Field(None, alias="autoStop")
    auto_pause: Optional[int] = Field(None, alias="autoPause")
    description: Optional[str] = Field(None, alias="description")
    workers_quantity: Optional[int] = Field(None, alias="workersQuantity")
    instance_role_uuid: Optional[str] = Field(None, alias="instanceRoleUUID")
    instance_type: Optional[str] = Field(None, alias="instanceType")
    bodo_version: Optional[str] = Field(None, alias="bodoVersion")
    auto_az: Optional[bool] = Field(True, alias="autoAZ")
    availability_zone: Optional[str] = Field(None, alias="availabilityZone")


class ClusterList(CamelCaseBase):
    data: List[ClusterResponse]
    metadata: PageMetadata


class ClusterPriceExportResponse(CamelCaseBase):
    """
    Job run price export response

    ...

    Attributes
    ----------
    url: str
        String to S3 bucket with the price export data
    """

    url: str


class ClusterPricingResponse(CamelCaseBase):
    """
    Represents a response for a list of job run pricings.

    Attributes:
    clusterWorkersQuantity (int): The quantity of workers in the cluster.
    clusterInstanceType (str): The instance type of the cluster.
    clusterName (str): The name of the cluster.
    clusterUseSpotInstance (bool): Indicates whether the cluster uses spot instances.
    workspaceName (str): The name of the workspace.
    startedAt (date): The start time of the cluster.
    finishedAt (date): The finish time of the cluster.
    bodoHourlyRate (float): The hourly rate for Bodo.
    duration (float): The duration of the cluster in hours.
    instancePrice (float): The price per instance.
    totalAWSPrice (float): The total AWS price for the cluster.
    totalBodoPrice (float): The total Bodo price for the cluster.
    """

    cluster_workers_quantity: int = Field(..., alias="clusterWorkersQuantity")
    cluster_instance_type: str = Field(..., alias="clusterInstanceType")
    cluster_name: str = Field(..., alias="clusterName")
    cluster_use_spot_instance: bool = Field(..., alias="clusterUseSpotInstance")
    workspace_name: str = Field(..., alias="workspaceName")
    started_at: date = Field(..., alias="startedAt")
    finished_at: date = Field(..., alias="finishedAt")
    bodo_hourly_rate: float = Field(..., alias="bodoHourlyRate")
    duration: float
    instance_price: float = Field(..., alias="instancePrice")
    total_aws_price: float = Field(..., alias="totalAWSPrice")
    total_bodo_price: float = Field(..., alias="totalBodoPrice")
