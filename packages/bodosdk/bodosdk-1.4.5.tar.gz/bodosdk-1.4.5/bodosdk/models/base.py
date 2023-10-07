import enum
from enum import Enum
from typing import Optional

import pydantic
from pydantic import Field


class CamelCaseBase(pydantic.BaseModel):
    class Config:
        allow_population_by_field_name = True


class APIKeys(pydantic.BaseModel):
    """
    Class representing Bodo Platform API keys used for auth token generation
    """

    client_id: str
    secret_key: str


class WorkspaceKeys(APIKeys):
    pass


class OrganizationKeys(APIKeys):
    pass


class PersonalKeys(APIKeys):
    pass


class JobStatus(enum.Enum):
    """
    List of possible job statuses
    NEW - when job was saved in platform but not run yet
    INPROGRESS - when job is executed
    FINISHED - when job execution has finished
    FAILED - when job execution has failed
    """

    NEW = "NEW"
    INPROGRESS = "INPROGRESS"
    FINISHED = "FINISHED"
    FAILED = "FAILED"

    def __str__(self):
        return str(self.value)


class ClusterStatus(enum.Enum):
    """
    List of possible cluster statuses
    NEW - when cluster was saved but creation process hasn't started
    INPROGRESS - when operation on cluster is performed
    ASGCREATED - AWS specific state, means that asg with 0 machines was created
    SCALING - AWS specific state, means that machines are scaled up or dawn
    RUNNING - when cluster is ready for use
    FAILED - when something went wrong with cluster operations
    TERMINATING - when deletion is in progress
    PAUSED - when machines are stopped, may be started again
    PAUSING - when operation of stopping machines is in progress
    RESUMING - when operation of starting machines is in progress
    STOPPING - when operation of stopping machines is in progress
    STOPPED - when machines are stopped
    RESTARTING - when operation of restarting machines is in progress
    """

    NEW = "NEW"
    INPROGRESS = "INPROGRESS"
    ASGCREATED = "ASGCREATED"
    INITIALIZING = "INITIALIZING"
    SCALING = "SCALING"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    TERMINATING = "TERMINATING"
    TERMINATED = "TERMINATED"
    PAUSED = "PAUSED"
    PAUSING = "PAUSING"
    RESUMING = "RESUMING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    RESTARTING = "RESTARTING"

    def __str__(self):
        return str(self.value)


class TaskStatus(Enum):
    """
    List of possible tasks statuses, common for all resources.
    Tasks are operations of creating, removing, pausing/resuming resources or executing jobs

    """

    NEW = "NEW"
    QUEUED = "QUEUED"
    INPROGRESS = "INPROGRESS"
    FINISHED = "FINISHED"
    FAILED = "FAILED"

    def __str__(self):
        return str(self.value)


class CloudConfigStatus(Enum):
    ACTIVE = "ACTIVE"
    INCOMPLETE = "INCOMPLETE"

    def __str__(self):
        return str(self.value)


class BodoRole(Enum):
    ADMIN = "BodoAdmin"
    VIEWER = "BodoViewer"

    def __str__(self):
        return str(self.value)


class WorkspaceStatus(Enum):
    NEW = "NEW"
    INPROGRESS = "INPROGRESS"
    READY = "READY"
    FAILED = "FAILED"
    TERMINATING = "TERMINATING"
    TERMINATED = "TERMINATED"

    def __str__(self):
        return str(self.value)


class TaskInfo(CamelCaseBase):
    uuid: str
    status: TaskStatus
    task_type: str = Field(..., alias="taskType")
    logs: str


class PaginationOrder(str, enum.Enum):
    ASC = "ASC"
    DESC = "DESC"

    def __str__(self):
        return str(self.value)


class PageMetadata(CamelCaseBase):
    page: int
    size: int
    order: Optional[PaginationOrder]
    total_pages: int
    total_items: int
