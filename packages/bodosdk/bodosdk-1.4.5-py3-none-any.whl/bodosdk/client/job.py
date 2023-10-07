import logging
from copy import deepcopy
from datetime import datetime
from time import sleep
from typing import List, Union, Callable
from uuid import UUID

from bodosdk.api.job import JobApi
from bodosdk.exc import ResourceNotFound, Unauthorized, WaiterTimeout
from bodosdk.models import JobStatus
from bodosdk.models.job import (
    JobDefinition,
    JobResponse,
    JobExecution,
    JobCreateResponse,
    BatchJobDefinitionResponse,
    CreateBatchJobDefinition,
    JobRunResponse,
    JobRunType,
    CreateJobRun,
    JobRunStatus,
    CreateSQLJobRun,
    JobRunLogsResponse,
)
from bodosdk.models.base import PaginationOrder


class JobWaiter:
    def __init__(self, client, job_run=False):
        """
        Object for waiting till job finishes

        :param client:
        :type client: JobClient
        """
        self._client = client
        self._is_job_run = job_run

    def wait(
        self,
        uuid,
        on_success: Callable = None,
        on_failure: Callable = None,
        on_timeout: Callable = None,
        check_period=10,
        timeout=None,
    ):
        """
        Method to wait for specific job to finished, returns job object or results of callbacks if defined

        :param uuid: job uuid
        :param on_success: callback to be called on success, job object is passed into
        :param on_failure: callback to be called on failure, job object is passed into
        :param on_timeout: callback to be called on failure, job uuid passed into.
        If no callback WaiterTimeout exception raised
        :param check_period: how often waiter should check
        :param timeout: how long waiter should try, None means infinity
        :return: job response or result of callbacks
        :raises WaiterTimeout: when timeout and no on_timeout callback defined
        """
        job = self.get_job_by_uuid(uuid)
        while not self.termination_condition(job, job.status):
            sleep(check_period)
            timeout = timeout - check_period if timeout else timeout
            if timeout is not None and timeout <= 0:
                if on_timeout:
                    return on_timeout(uuid)
                raise WaiterTimeout
            job = self.get_job_by_uuid(uuid)

        if (job.status == JobStatus.FINISHED and on_success) or (
            job.status == JobRunStatus.SUCCEEDED and on_success
        ):
            return on_success(job)
        if (job.status == JobStatus.FAILED and on_failure) or (
            job.status == JobRunStatus.FAILED and on_failure
        ):
            return on_failure(job)
        return job

    def get_job_by_uuid(self, uuid):
        return (
            self._client.get_batch_job_run(uuid)
            if self._is_job_run
            else self._client.get(uuid)
        )

    def termination_condition(self, job, status):
        if isinstance(status, JobRunStatus):
            job: JobRunStatus = job
            return job.status in (
                JobRunStatus.FAILED,
                JobRunStatus.SUCCEEDED,
                JobRunStatus.CANCELLED,
            )
        return job.status in (JobStatus.FINISHED, JobStatus.FAILED)  # for jobs v2


class JobClient:
    def __init__(self, api: JobApi):
        self._api = api

    def create(self, job_definition: JobDefinition) -> JobCreateResponse:
        """
        Creates a job and job dedicated cluster

        :param job_definition:
            definition of job and cluster
        :type job_definition: JobDefinition
        :return: created job data
        :rtype: JobDefinition
        :raises Unauthorized: when keys are invalid
        :raises ValidationError: when JobDefinition is invalid
        """
        try:
            return self._api.create_job(job_definition)
        except ResourceNotFound:
            raise Unauthorized

    def remove(self, job_uuid: Union[str, UUID]) -> None:
        """
        Removes job and it's cluster

        :param job_uuid:
        :type job_uuid: Union[str, UUID]
        :return: None
        :rtype: None
        :raises ResourceNotFound:
        """
        self._api.delete_job(str(job_uuid))

    def list(self) -> List[JobResponse]:
        """
        List all jobs in workspace

        :return: list of jobs
        :rtype: List[JobResponse]
        """
        return self._api.list_jobs()

    def get(self, uuid: Union[str, UUID]) -> JobResponse:
        """
        Gets specific job from workspace

        :param uuid:
        :type uuid: Union[str, UUID]
        :return: job data
        :rtype: JobResponse
        :raises ResourceNotFound:
        """
        return self._api.get_job(str(uuid))

    def get_job_executions(self, uuid: Union[str, UUID]) -> List[JobExecution]:
        """
        Returns job executions for specific job

        :param uuid:
        :type uuid: Union[str, UUID]
        :return: list of job executions
        :rtype: List[JobExecution]
        :raises ResourceNotFound:
        """
        return self._api.get_tasks(str(uuid))

    def get_waiter(self) -> JobWaiter:
        """
        Returns waiter waiting till the job finishes, given a workspace
        :return: a helper waiting till job finishes
        :rtype: JobWaiter
        """
        return JobWaiter(client=deepcopy(self))

    def get_job_run_waiter(self) -> JobWaiter:
        """
        Returns a waiter that waits until the job run finishes
        Designed for V3 jobs usage
        :return: a helper waiting till job finishes
        :rtype: JobWaiter
        """
        return JobWaiter(client=deepcopy(self), job_run=True)

    def list_batch_job_definitions(
        self, page: int, page_size: int, order: PaginationOrder
    ) -> List[BatchJobDefinitionResponse]:
        """
        List all batch job definitions in workspace

        :return: list of batch job definitions
        :rtype: List[BatchJobDefinition]
        """
        list_batch_job_definitions = self._api.list_batch_job_definitions(
            page, page_size, order
        )
        if len(list_batch_job_definitions) == 0:
            logging.warning("No batch job definitions found. Please create one.")
        return list_batch_job_definitions

    def get_batch_job_definition(
        self, uuid: Union[str, UUID]
    ) -> BatchJobDefinitionResponse:
        """
        Gets specific batch job definition from workspace

        :param uuid:
        :type uuid: Union[str, UUID]
        :return: batch job definition
        :rtype: BatchJobDefinition
        :raises ResourceNotFound:
        """
        try:
            return self._api.get_batch_job_definition(uuid)
        except Exception as exception:
            raise exception

    def get_batch_job_definition_by_name(self, name: str) -> BatchJobDefinitionResponse:
        """
        Gets specific batch job definition from workspace

        :param name:
        :type name: str
        :return: batch job definition
        :rtype: BatchJobDefinition
        :raises ResourceNotFound:
        """
        try:
            return self._api.get_batch_job_definition_by_name(name)
        except Exception as exception:
            raise exception

    def create_batch_job_definition(
        self, create_batch_job_definition: CreateBatchJobDefinition
    ) -> BatchJobDefinitionResponse:
        """
        Creates a batch job definition

        :param create_batch_job_definition:
            definition of batch job
        :type create_batch_job_definition: CreateBatchJobDefinition
        :return: created batch job definition
        :rtype: BatchJobDefinition
        :raises Unauthorized: when keys are invalid
        :raises ValidationError: when BatchJobDefinition is invalid
        """
        try:
            return self._api.create_batch_job_definition(create_batch_job_definition)
        except Exception as exception:
            raise exception

    def remove_batch_job_definition(self, uuid: Union[str, UUID]) -> None:
        """
        Removes batch job definition

        :param uuid:
        :type uuid: Union[str, UUID]
        :return: None
        :rtype: None
        :raises ResourceNotFound:
        """
        try:
            self._api.delete_batch_job_definition(uuid)
        except Exception as exception:
            raise exception

    def list_batch_job_runs(
        self,
        batch_job_ids: List[UUID] = None,
        statuses: List[JobRunStatus] = None,
        cluster_ids: List[UUID] = None,
        started_at: datetime = None,
        finished_at: datetime = None,
        page: int = 1,
        page_size: int = 10,
        order: PaginationOrder = PaginationOrder.ASC,
    ) -> List[JobRunResponse]:
        batch_job_runs = self._api.list_job_runs(
            type=[JobRunType.BATCH],
            batchJobDefinitionUUID=batch_job_ids,
            status=statuses,
            clusterUUID=cluster_ids,
            startedAt=started_at,
            finishedAt=finished_at,
            page=page,
            size=page_size,
            order=order,
        )

        if len(batch_job_runs) == 0:
            logging.warning("No batch job runs found.")
        return batch_job_runs

    def list_job_runs_by_batch_job_name(
        self,
        batch_job_names: List[str] = None,
        statuses: List[JobRunStatus] = None,
        cluster_ids: List[UUID] = None,
        started_at: datetime = None,
        finished_at: datetime = None,
        page: int = 1,
        page_size: int = 10,
        order: PaginationOrder = PaginationOrder.ASC,
    ) -> List[JobRunResponse]:
        """
        List all batch job runs in workspace using batch job name

        :param batch_job_names:
        :type batch_job_names: List[str]
        :param statuses:
        :type statuses: List[JobRunStatus]
        :param cluster_ids:
        :type cluster_ids: List[UUID]
        :param started_at:
        :type started_at: datetime
        :param finished_at:
        :type finished_at: datetime
        :param page:
        :type page: int
        :param page_size:
        :type page_size: int
        :param order:
        :type order: PaginationOrder
        :return: list of batch job runs
        :rtype: List[JobRunResponse]

        """
        batch_job_ids = []
        for name in batch_job_names:
            batch_job_def_uuid = self.get_batch_job_definition_by_name(name).uuid
            batch_job_ids.append(batch_job_def_uuid)

        batch_job_runs = self._api.list_job_runs(
            type=[JobRunType.BATCH],
            batchJobDefinitionUUID=batch_job_ids,
            status=statuses,
            clusterUUID=cluster_ids,
            startedAt=started_at,
            finishedAt=finished_at,
            page=page,
            size=page_size,
            order=order,
        )
        return batch_job_runs

    def get_batch_job_run(self, uuid: Union[str, UUID]) -> JobRunResponse:
        """
        Gets specific batch job run from workspace

        :param uuid:
        :type uuid: Union[str, UUID]
        :return: batch job run
        :rtype: JobRunResponse
        :raises ResourceNotFound:
        """
        try:
            return self._api.get_job_run(uuid)
        except Exception as exception:
            raise exception

    def submit_batch_job_run(
        self, create_batch_job_run: CreateJobRun
    ) -> JobRunResponse:
        """
        Creates a batch job run

        :param create_batch_job_run:
            definition of batch job run
        :type create_batch_job_run: CreateBatchJobRun
        :return: created batch job run
        :rtype: JobRunResponse
        :raises Unauthorized: when keys are invalid
        :raises ValidationError: when BatchJobRun is invalid
        """
        try:
            job_run = self._api.create_batch_job_run(create_batch_job_run)
            logging.info(f"Batch job run {job_run.uuid} submitted.")
            return job_run
        except Exception as exception:
            raise exception

    def check_job_run_status(
        self, batch_job_run_uuid: Union[str, UUID]
    ) -> JobRunStatus:
        """
        Checks status of batch job run

        :param batch_job_run_uuid:
        :type batch_job_run_uuid: Union[str, UUID]
        :return: status of batch job run
        :rtype: JobRunStatus
        :raises ResourceNotFound:
        """
        try:
            job_run = self._api.get_job_run(batch_job_run_uuid)
            return job_run.status
        except Exception as exception:
            raise exception

    def submit_sql_job_run(self, create_sql_job_run: CreateSQLJobRun) -> JobRunResponse:
        """
        Creates a sql job run

        :param create_sql_job_run:
            definition of sql job run
        :type create_sql_job_run: CreateSQLJobRun
        :return: created sql job run
        :rtype: JobRunResponse
        :raises Unauthorized: when keys are invalid
        :raises ValidationError: when SqlJobRun is invalid
        """
        try:
            job_run = self._api.create_sql_job_run(create_sql_job_run)
            logging.info(f"Sql job run {job_run.uuid} submitted.")
            return job_run
        except Exception as exception:
            raise exception

    def cancel_batch_job_run(self, uuid: Union[str, UUID]) -> None:
        """
        Cancels batch job run

        :param uuid:
        :type uuid: Union[str, UUID]
        :return: None
        :rtype: None
        :raises ResourceNotFound:
        """
        try:
            self._api.cancel_batch_job_run(uuid)
        except Exception as exception:
            raise exception

    def cancel_all_job_runs(self, cluster_uuids: Union[List[str], List[UUID]] = None):
        """
        Cancels all job runs in workspace or for specified clusters
        :return: None
        """
        try:
            self._api.cancel_all_job_runs(cluster_uuids)
        except Exception as exception:
            raise exception

    def get_job_logs(
        self, uuid: Union[str, UUID], force_refresh=False
    ) -> JobRunLogsResponse:
        """
        Procures stdout and stderr url links and downloads them for a given job

        :param force_refresh:
        :param uuid:
        :type uuid: Union[str, UUID]
        :return: stdoutURL stderrURL & Expiration_ts
        :rtype: JobRunLogsResponse
        :raises ResourceNotFound:
        """
        try:
            return self._api.get_job_log_links(uuid, force_refresh)
        except Exception as exception:
            raise exception
