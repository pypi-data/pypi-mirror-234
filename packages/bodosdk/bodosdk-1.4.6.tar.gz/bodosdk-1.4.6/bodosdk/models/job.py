import enum
from datetime import date, datetime
from typing import Optional, Dict, Union, List
from uuid import UUID

import pydantic
from pydantic import Field, root_validator

from bodosdk.models.base import JobStatus, TaskStatus, CamelCaseBase, PaginationOrder


class JobClusterDefinition(CamelCaseBase):
    instance_type: str = Field(..., alias="instanceType")
    workers_quantity: int = Field(..., alias="workersQuantity")
    accelerated_networking: bool = Field(..., alias="acceleratedNetworking")
    image_id: Optional[str] = Field(None, alias="imageId")
    bodo_version: Optional[str] = Field(None, alias="bodoVersion")
    instance_role_uuid: Optional[str] = Field(None, alias="instanceRoleUUID")
    availability_zone: Optional[str] = Field(None, alias="availabilityZone")
    aws_deployment_subnet_id: Optional[str] = Field(None, alias="awsDeploymentSubnetId")
    custom_tags: Optional[Dict[str, str]] = Field(None, alias="customTags")
    auto_pause: Optional[int] = Field(60, alias="autoPause")
    auto_stop: Optional[int] = Field(0, alias="autoStop")


class JobCluster(pydantic.BaseModel):
    uuid: Union[str, UUID]


class JobSourceType(enum.Enum):
    GIT = "GIT"
    S3 = "S3"
    WORKSPACE = "WORKSPACE"
    SQL = "SQL"

    def __repr__(self):
        return self.value

    def __str__(self):
        return str(self.value)


class GitRepoSource(CamelCaseBase):
    """
    Git repository source definition.

    ...

    Attributes
    ----------
    repo_url: str
        Git repository URL.

    reference: Optional[str]
        Git reference (branch, tag, commit hash). (Default: "")

    username: str
        Git username.

    token: str
        Git token.

    """

    type: JobSourceType = Field(JobSourceType.GIT, const=True)
    repo_url: str = Field(..., alias="repoUrl")
    reference: Optional[str] = ""
    username: str
    token: str


class S3Source(CamelCaseBase):
    """
    S3 source definition.

    ...

    Attributes
    ----------
    bucket_path: str
        S3 bucket path.

    bucket_region: str
        S3 bucket region.

    """

    type: JobSourceType = Field(JobSourceType.S3, const=True)
    bucket_path: str = Field(..., alias="bucketPath")
    bucket_region: str = Field(..., alias="bucketRegion")


class WorkspaceSource(pydantic.BaseModel):
    """
    Workspace source definition.

    ...

    Attributes
    ----------
    path: str
        Workspace path.
    """

    type: JobSourceType = Field(JobSourceType.WORKSPACE, const=True)
    path: str


class SQLSource(CamelCaseBase):
    """
    SQL source definition.

    ...
    """

    type: JobSourceType = Field(JobSourceType.SQL, const=True)


class JobDefinition(CamelCaseBase):
    name: str
    args: str
    source_config: Union[GitRepoSource, S3Source, WorkspaceSource] = Field(
        ..., alias="sourceConfig"
    )
    cluster_object: Union[JobClusterDefinition, JobCluster] = Field(
        ..., alias="clusterObject"
    )
    variables: Dict = Field(default_factory=dict)
    timeout: Optional[int] = 120
    retries: Optional[int] = 0
    retries_delay: Optional[int] = Field(0, alias="retriesDelay")
    retry_on_timeout: Optional[bool] = Field(False, alias="retryOnTimeout")


class JobClusterResponse(CamelCaseBase):
    uuid: Optional[str] = None
    name: str
    instance_type: str = Field(..., alias="instanceType")
    workers_quantity: int = Field(..., alias="workersQuantity")
    accelerated_networking: bool = Field(..., alias="acceleratedNetworking")
    bodo_version: Optional[str] = Field(None, alias="bodoVersion")
    image_id: str = Field(..., alias="imageId")


class JobResponse(CamelCaseBase):
    uuid: UUID
    name: str
    status: JobStatus
    schedule: datetime
    command: str
    variables: Dict
    workspace_path: Optional[str] = Field(None, alias="workspacePath")
    workspace_reference: Optional[str] = Field(None, alias="workspaceReference")
    cluster: Optional[JobClusterResponse] = None


class JobCreateResponse(CamelCaseBase):
    uuid: UUID
    status: JobStatus
    name: str
    args: str
    variables: Dict
    source_config: Union[GitRepoSource, S3Source, WorkspaceSource] = Field(
        ..., alias="sourceConfig"
    )
    cluster_config: Union[JobClusterDefinition, JobCluster] = Field(
        ..., alias="clusterConfig"
    )
    cluster: Optional[JobClusterResponse] = None
    variables: Dict = Field(default_factory=dict)
    timeout: Optional[int] = 120
    retries: Optional[int] = 0
    retries_delay: Optional[int] = Field(0, alias="retriesDelay")
    retry_on_timeout: Optional[bool] = Field(False, alias="retryOnTimeout")


class JobRunLogsResponse(CamelCaseBase):
    stderr_location_url: str = Field(None, alias="stderrUrl")
    stdout_location_url: str = Field(None, alias="stdoutUrl")
    expiration_date: str = Field(None, alias="expirationDate")


class JobExecution(CamelCaseBase):
    uuid: UUID
    status: TaskStatus
    logs: str
    modify_date: datetime = Field(..., alias="modifyDate")
    created_at: datetime = Field(..., alias="createdAt")


class JobSource(CamelCaseBase):
    """
    Job source.

    ...

    Attributes
    ----------
    type: JobSourceType
        Job source type.

    definition: Union[GitDef, S3Def, WorkspaceDef]
        Job source definition.
    """

    type: JobSourceType
    definition: Union[GitRepoSource, S3Source, WorkspaceSource, SQLSource] = Field(
        ..., alias="sourceDef"
    )


class RetryStrategy(CamelCaseBase):
    """
    Retry strategy for a job.

    ...

    Attributes
    ----------
    num_retries: int
        Number of retries for a job. (Default: 0)

    delay_between_retries: int
        Delay between retries in minutes. (Default: 1)

    retry_on_timeout: bool
        Retry on timeout. (Default: False)

    """

    num_retries: int = Field(0, alias="numRetries")
    delay_between_retries: int = Field(1, alias="delayBetweenRetries")  # in minutes
    retry_on_timeout: bool = Field(False, alias="retryOnTimeout")


class SourceCodeType(enum.Enum):
    PYTHON = "PYTHON"
    IPYNB = "IPYNB"
    SQL = "SQL"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


class JobConfig(CamelCaseBase):
    """
    Job configuration.

    ...

    Attributes
    ----------
    source: JobSource
        Job source.

    source_code_type: SourceCodeType
        Job source code type.

    sourceLocation: Optional[str]
        Job source location.

    args: Union[str, Dict]
        Job arguments. (Default: {})

    retry_strategy: Optional[RetryStrategy]
        Job retry strategy. (Default: {num_retries: 0, delay_between_retries: 1, retry_on_timeout: False})

    timeout: int
        Job timeout in minutes. (Default: 60)

    env_vars: Dict
        Job environment variables. (Default: {})

    catalog: Optional[str]
        Catalog name. (Default: None)

    """

    source: JobSource
    source_code_type: SourceCodeType = Field(..., alias="type")
    sourceLocation: Optional[str]
    args: Union[str, Dict, None] = Field(default_factory=dict)
    retry_strategy: Optional[RetryStrategy] = Field(
        RetryStrategy(), alias="retryStrategy"
    )
    timeout: int = 60
    env_vars: Union[None, Dict] = Field(default_factory=dict, alias="envVars")
    catalog: Optional[str] = None

    def __repr__(self):
        repr_str = ""
        for k, v in self.dict().items():
            if v is not None:
                repr_str += f"{k}: {v}\n"
            else:
                repr_str += f"{k}: None\n"
        return repr_str[:-1]  # remove last newline

    def __str__(self):
        return self.__repr__()


class JobConfigOverride(CamelCaseBase):
    """
    Job configuration override.

    ...

    Attributes
    ----------
    source: Optional[JobSource]
        Job source.

    type: Optional[SourceCodeType]
        Job source code type.

    sourceLocation: Optional[str]
        Job source location.

    args: Optional[Union[str, Dict]]
        Job arguments. (Default: {})

    retry_strategy: Optional[RetryStrategy]
        Job retry strategy. (Default: {num_retries: 0, delay_between_retries: 1, retry_on_timeout: False})

    timeout: Optional[int]
        Job timeout in minutes. (Default: 60)

    env_vars: Optional[Dict]
        Job environment variables. (Default: {})
    """

    source: Optional[JobSource]
    type: Optional[SourceCodeType]
    sourceLocation: Optional[str]
    args: Optional[Union[str, Dict]] = Field(default_factory=dict)
    retry_strategy: Optional[RetryStrategy] = Field(
        RetryStrategy(), alias="retryStrategy"
    )
    timeout: Optional[int] = 60
    env_vars: Optional[Dict] = Field(default_factory=dict, alias="envVars")


class CreateBatchJobDefinition(CamelCaseBase):
    """
    Batch job definition.

    ...

    Attributes
    ----------
    description: str
        Job definition description.

    config: JobConfig
        Job configuration.

    cluster_config: JobClusterDefinition
        Job cluster configuration.

    """

    name: str
    description: str
    config: JobConfig
    cluster_config: Optional[JobClusterDefinition] = Field(
        default=None, alias="clusterConfig"
    )


class JobRunType(str, enum.Enum):
    BATCH = "BATCH"
    INTERACTIVE = "INTERACTIVE"

    def __str__(self):
        return str(self.value)


class JobRunStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    CANCELLING = "CANCELLING"
    TIMED_OUT = "TIMEOUT"

    def __repr__(self):
        return self.value

    def __str__(self):
        return str(self.value)


class BatchJobDefinitionUUID(CamelCaseBase):
    """
    Batch job definition response wit uuid only.

    ...

    Attributes
    ----------
    uuid: UUID
        Job definition ID.
    """

    uuid: UUID


class JobRunPriceExportResponse(CamelCaseBase):
    """
    Job run price export response

    ...

    Attributes
    ----------
    url: str
        String to S3 bucket with the price export data
    """

    url: str


class JobRunPricingResponse(CamelCaseBase):
    """
    Represents a response object for job run pricing information.

    Attributes:
    name (str): The name of the job.
    jobRunUUID (str): The UUID of the job run.
    batchJobDefinitionUUID (str): The UUID of the batch job definition.
    clusterWorkersQuantity (int): The quantity of cluster workers.
    clusterInstanceType (str): The instance type of the cluster.
    clusterName (str): The name of the cluster.
    sqlQuery (str): The SQL query executed by the job.
    clusterUseSpotInstance (bool): Indicates whether the cluster uses spot instances.
    startedAt (date): The start date of the job run.
    inishedAt (date): The end date of the job run.
    status (str): The status of the job run.
    duration (float): The duration of the job run in seconds.
    instancePrice (float): The price per instance.
    bodoHourlyRate (float): The hourly rate for using Bodo.
    totalAWSPrice (float): The total price charged by AWS.
    totalBodoPrice (float): The total price charged by Bodo.
    """

    name: str
    job_run_uuid: str = Field(..., alias="jobRunUUID")
    batch_job_definition_uuid: str = Field(..., alias="batchJobDefinitionUUID")
    cluster_workers_quantity: int = Field(..., alias="clusterWorkersQuantity")
    cluster_instance_type: str = Field(..., alias="clusterInstanceType")
    cluster_name: str = Field(..., alias="clusterName")
    sql_query: str = Field(..., alias="sqlQuery")
    cluster_use_spot_instance: bool = Field(..., alias="clusterUseSpotInstance")
    started_at: date = Field(..., alias="startedAt")
    finished_at: date = Field(..., alias="finishedAt")
    status: str
    duration: float
    instance_price: float = Field(..., alias="instancePrice")
    bodo_hourly_rate: float = Field(..., alias="bodoHourlyRate")
    total_aws_price: float = Field(..., alias="totalAWSPrice")
    total_bodo_price: float = Field(..., alias="totalBodoPrice")


class JobRunResponse(CamelCaseBase):
    """
    Job run response.

    ...

    Attributes
    ----------
    uuid: UUID
        Job run ID.

    name: str
        Job run name.

    clusterUUID: UUID
        Job run cluster ID.

    type: JobRunType
        Job run type.

    config: JobConfig
        Job run configuration.

    submittedAt: datetime
        Job run submission time.

    finishedAt: datetime
        Job run finish time.

    startedAt: datetime
        Job run start time.

    status: JobRunStatus
        Job run status.

    batchJobDefinitionConfigOverrides: Optional[JobConfigOverride]
        Job run batch job definition configuration overrides.

    numRetriesUsed: int
        Number of retries used.

    lastHealthCheck: Optional[datetime]
        Job run last health check.

    lastKnownActivity: Optional[datetime]
        Job run last known activity.

    """

    uuid: UUID
    name: str
    clusterUUID: Optional[Union[UUID, None]] = Field(default=None, alias="clusterUUID")
    cluster: Optional[JobCluster]
    type: JobRunType
    config: JobConfig
    submittedAt: datetime = Field(..., alias="submittedAt")
    finishedAt: Optional[Union[datetime, None]] = Field(
        default=None, alias="finishedAt"
    )
    startedAt: Optional[Union[datetime, None]] = Field(default=None, alias="startedAt")
    status: JobRunStatus
    batchJobDefinitionConfigOverrides: Optional[JobConfigOverride]
    batch_job_definition: Optional[BatchJobDefinitionUUID] = Field(
        None, alias="batchJobDefinition"
    )
    numRetriesUsed: int = Field(..., alias="numRetriesUsed")
    lastHealthCheck: Optional[Union[datetime, None]] = Field(
        default=None, alias="lastHealthCheck"
    )
    lastKnownActivity: Optional[Union[datetime, None]] = Field(
        default=None, alias="lastknownActivity"
    )
    reason: Optional[str]
    submitter: Optional[str]

    def __repr__(self):
        repr_string = ""
        for key, value in self.__dict__.items():
            if value is not None:
                repr_string += f"{key}: {value}\n"
            else:
                repr_string += f"{key}: None\n"
        return repr_string[:-1]  # remove last newline

    def __str__(self):
        return self.__repr__()


class BatchJobDefinitionResponse(BatchJobDefinitionUUID):
    """
    Batch job definition response.

    ...

    Attributes
    ----------
    uuid: UUID
        Job definition ID.

    name: str
        Job definition name.

    description: str
        Job definition description.

    config: JobConfig
        Job configuration.

    cluster_config: JobClusterDefinition
        Job cluster configuration.

    created_by: str
        Job definition creator.

    """

    name: str
    description: str
    config: JobConfig
    cluster_config: Optional[JobClusterDefinition] = Field(
        default=None, alias="clusterConfig"
    )
    created_by: Optional[str] = Field(alias="createdBy")
    job_runs: List[JobRunResponse] = Field(default_factory=list, alias="jobRuns")
    # Run related fields
    # Rules related fields


class CreateJobRun(CamelCaseBase):
    """
    Create job run.

    ...

    Attributes
    ----------
    type: JobRunType
        Job run type.

    clusterUUID: Optional[Union[UUID, str]]
        Job cluster UUID.

    batchJobUUID: Optional[Union[UUID, str]]
        Batch job UUID.

    batchJobName: Optional[str]

    batchJobDefinitionConfigOverrides: Optional[JobConfigOverride]
        Batch job definition configuration overrides.
    """

    type: JobRunType = JobRunType.BATCH
    clusterUUID: Optional[Union[UUID, str]]  # Todo(Ritwika): Confirm
    batchJobDefinitionUUID: Optional[Union[UUID, str]] = Field(
        default=None, alias="batchJobDefinitionUUID"
    )
    batchJobName: Optional[str] = Field(default=None, alias="batchJobName")
    batchJobDefinitionConfigOverrides: Optional[JobConfigOverride]

    @root_validator(pre=True)
    def validate_batch_job_def_id(cls, values):
        if not ("batchJobDefinitionUUID" in values.keys()):
            if not ("batchJobName" in values.keys()):
                raise ValueError(
                    "Either batchJobDefinitionUUID or batchJobName must be provided."
                )
        return values


class CreateSQLJobRun(CamelCaseBase):
    """
    Create SQL job run.

    ...

    Attributes
    ----------
    type: JobRunType
        Job run type.

    clusterUUID: Optional[str]
        Job cluster UUID.

    cluster_config: Optional[JobClusterDefinition]
        Job cluster configuration.

    catalog: str
        Catalog name.

    retry_strategy: Optional[RetryStrategy]
        Retry strategy.

    timeout: Optional[int]
        Job timeout in minutes. (Default: 60)

    env_vars: Optional[Dict]
        Job environment variables. (Default: {})

    sql_query_text: str
        SQL query text.

    query_tags: Optional[Dict]
        Query tags. (Default: {})
    """

    type: JobRunType = JobRunType.BATCH
    clusterUUID: Optional[Union[UUID, str]]
    cluster_config: Optional[JobClusterDefinition] = Field(
        default=None, alias="clusterConfig"
    )
    catalog: str
    retry_strategy: Optional[RetryStrategy] = Field(
        RetryStrategy(), alias="retryStrategy"
    )
    timeout: Optional[int] = 60
    env_vars: Optional[Dict] = Field(default_factory=dict, alias="envVars")
    sql_query_text: str = Field(..., alias="sqlQueryText")
    query_tags: Optional[Dict] = Field(default_factory=dict, alias="queryTags")


DEFAULT_PAGE_SIZE = 5
DEFAULT_PAGE = 1
DEFAULT_ORDER = PaginationOrder.ASC

LIST_QUERY_PARAMS = [
    "type",
    "batchJobDefinitionUUID",
    "status",
    "clusterUUID",
    "startedAt",
    "finishedAt",
    "page",
    "size",
    "order",
]
