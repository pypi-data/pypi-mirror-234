import logging
from datetime import datetime
from typing import List, Union
from uuid import UUID
from bodosdk.error_handlers.handle_api_error import handle_job_run_api_error

import pydantic.error_wrappers
from pydantic import validate_arguments

from bodosdk.api.base import BackendApi
from bodosdk.exc import (
    ResourceNotFound,
    ServiceUnavailable,
    UnknownError,
    ValidationError,
)
from bodosdk.models.job import (
    LIST_QUERY_PARAMS,
    DEFAULT_PAGE,
    DEFAULT_PAGE_SIZE,
    DEFAULT_ORDER,
)
from bodosdk.models.base import PaginationOrder
from bodosdk.models.job import (
    JobDefinition,
    JobResponse,
    JobExecution,
    JobCreateResponse,
    CreateBatchJobDefinition,
    BatchJobDefinitionResponse,
    JobConfigOverride,
    JobRunResponse,
    JobRunType,
    CreateJobRun,
    JobRunStatus,
    CreateSQLJobRun,
    JobRunLogsResponse,
)


# helper function to compose query string from query parameters
def build_query_string(args):
    query_params = []
    for k, v in args.items():
        if v is not None:
            if isinstance(v, list) and v:
                param = f"{k}[]={','.join(f'{x}' for x in v)}"
            elif not isinstance(v, list):
                param = f"{k}={v}"
            else:
                continue
            query_params.append(param)
    if query_params:
        return "?" + "&".join(query_params)
    return ""


def handle_pydantic_validation_issues_for_batch_job_def_response_json(response_json):
    try:
        return BatchJobDefinitionResponse(**response_json)
    except pydantic.ValidationError:
        logging.error(
            f"Failed to parse batch job definition for batch job id: {response_json['uuid']}"
        )
    except Exception as e:
        logging.error(f"Bad Response: {e}")


class JobApi(BackendApi):
    def __init__(self, *args, **kwargs):
        super(JobApi, self).__init__(*args, **kwargs)
        self._resource_url = "job"

    def create_job(self, job_definition: JobDefinition) -> JobCreateResponse:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            self.get_resource_url("v2"),
            data=job_definition.json(by_alias=True),
            headers=headers,
        )
        if str(resp.status_code).startswith("2"):
            # remap list of variables to dict
            json_data = resp.json()
            if isinstance(json_data["variables"], list):
                json_data["variables"] = {
                    k[0].strip(): k[1].strip()
                    for k in (item.split("=", 1) for item in json_data["variables"])
                }
            return JobCreateResponse(**json_data)
        if resp.status_code == 404:
            raise ResourceNotFound("Probably wrong workspace keys")
        if resp.status_code in (400, 422):
            raise ValidationError(resp.json())
        if resp.status_code == 503:
            raise ServiceUnavailable
        if resp.status_code == 409:
            raise ServiceUnavailable(
                "There is probably a job running on the cluster. \
                Please wait for the existing job to finish and retry again later."
            )
        raise UnknownError

    def delete_job(self, job_uuid) -> None:
        headers = self.get_auth_header()
        resp = self._requests.delete(
            f"{self.get_resource_url()}/{job_uuid}", headers=headers
        )
        if resp.status_code == 200:
            return
        if resp.status_code == 404:
            raise ResourceNotFound
        if resp.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError(resp.content)

    def list_jobs(self) -> List[JobResponse]:
        headers = self.get_auth_header()
        resp = self._requests.get(
            f"{self.get_resource_url()}?withTasks=false", headers=headers
        )
        if resp.status_code == 503:
            raise ServiceUnavailable
        result = []
        for json_data in resp.json():
            # remap list of variables to dict
            if isinstance(json_data["variables"], list):
                json_data["variables"] = {
                    k[0]: k[1]
                    for k in (item.split("=", 1) for item in json_data["variables"])
                }
            result.append(JobResponse(**json_data))
        return result

    def get_job(self, uuid) -> JobResponse:
        headers = self.get_auth_header()
        resp = self._requests.get(f"{self.get_resource_url()}/{uuid}", headers=headers)
        if resp.status_code == 404:
            raise ResourceNotFound
        if resp.status_code == 503:
            raise ServiceUnavailable
        json_data = resp.json()
        if isinstance(json_data["variables"], list):
            # remap list of variables to dict
            json_data["variables"] = {
                k[0]: k[1]
                for k in (item.split("=", 1) for item in json_data["variables"])
            }
        return JobResponse(**json_data)

    def get_tasks(self, uuid) -> List[JobExecution]:
        headers = self.get_auth_header()
        resp = self._requests.get(
            f"{self.get_resource_url()}/{uuid}/tasks", headers=headers
        )
        handle_job_run_api_error(
            resp
        )  # raise exception if resp contains error code else continue normal execution if not
        return [JobExecution(**data) for data in resp.json()]

    @validate_arguments
    def create_batch_job_definition(
        self, job_definition: CreateBatchJobDefinition
    ) -> BatchJobDefinitionResponse:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            f"{self.get_resource_url()}/batch_job_def",
            data=job_definition.json(by_alias=True),
            headers=headers,
        )
        handle_job_run_api_error(resp)

        return BatchJobDefinitionResponse(**resp.json())

    @validate_arguments
    def delete_batch_job_definition(self, batch_job_definition_uuid: UUID) -> None:
        headers = self.get_auth_header()
        resp = self._requests.delete(
            f"{self.get_resource_url()}/batch_job_def/{batch_job_definition_uuid}",
            headers=headers,
        )
        handle_job_run_api_error(resp)

    # Todo: add query semantics for filtering
    @validate_arguments
    def list_batch_job_definitions(
        self,
        page: int = DEFAULT_PAGE,
        size: int = DEFAULT_PAGE_SIZE,
        order: PaginationOrder = DEFAULT_ORDER,
    ) -> List[BatchJobDefinitionResponse]:
        query_string_args = {
            k: v
            for k, v in locals().items()
            if v is not None and k in LIST_QUERY_PARAMS
        }
        headers = self.get_auth_header()
        resource_url = f"{self.get_resource_url()}/batch_job_def{build_query_string(query_string_args)}"
        resp = self._requests.get(resource_url, headers=headers)
        handle_job_run_api_error(resp)

        result = []
        for json_data in resp.json()["data"]:
            batch_job_def = (
                handle_pydantic_validation_issues_for_batch_job_def_response_json(
                    json_data
                )
            )
            if batch_job_def:
                result.append(batch_job_def)
        return result

    @validate_arguments
    def get_batch_job_definition(self, uuid: UUID) -> BatchJobDefinitionResponse:
        headers = self.get_auth_header()
        resp = self._requests.get(
            f"{self.get_resource_url()}/batch_job_def/{uuid}", headers=headers
        )
        handle_job_run_api_error(resp)

        json_data = resp.json()
        return handle_pydantic_validation_issues_for_batch_job_def_response_json(
            json_data
        )

    @validate_arguments
    def get_batch_job_definition_by_name(self, name: str) -> BatchJobDefinitionResponse:
        headers = self.get_auth_header()
        resp = self._requests.get(
            f"{self.get_resource_url()}/batch_job_def?name={name}", headers=headers
        )
        handle_job_run_api_error(resp)

        if not resp.json()["data"]:
            raise ResourceNotFound("Server returned null data")

        # Based on DB criteria there can be only one element
        for json_data in resp.json()["data"]:
            return handle_pydantic_validation_issues_for_batch_job_def_response_json(
                json_data
            )

    @validate_arguments
    def update_batch_job_definition(
        self, uuid: UUID, config_override: JobConfigOverride
    ) -> BatchJobDefinitionResponse:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.patch(
            f"{self.get_resource_url()}/batch_job_def/{uuid}",
            data=config_override.json(by_alias=True),
            headers=headers,
        )
        handle_job_run_api_error(resp)
        return BatchJobDefinitionResponse(**resp.json())

    # Job Run APIs
    @validate_arguments
    def create_batch_job_run(self, create_job_run: CreateJobRun) -> JobRunResponse:
        if not create_job_run.batchJobDefinitionUUID:
            batch_job_definition = self.get_batch_job_definition_by_name(
                create_job_run.batchJobName
            )
            create_job_run.batchJobDefinitionUUID = batch_job_definition.uuid
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            f"{self.get_resource_url()}/run/batch",
            data=create_job_run.json(by_alias=True),
            headers=headers,
        )
        handle_job_run_api_error(resp)
        return JobRunResponse(**resp.json())

    @validate_arguments
    def create_sql_job_run(self, create_sql_job_run: CreateSQLJobRun) -> JobRunResponse:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            f"{self.get_resource_url()}/run/sql",
            data=create_sql_job_run.json(by_alias=True),
            headers=headers,
        )
        handle_job_run_api_error(resp)
        return JobRunResponse(**resp.json())

    @validate_arguments
    def get_job_run(self, uuid: UUID, job_type: JobRunType = "BATCH") -> JobRunResponse:
        job_type_url_suffix = job_type.lower()
        headers = self.get_auth_header()
        resp = self._requests.get(
            f"{self.get_resource_url()}/run/{job_type_url_suffix}/{uuid}",
            headers=headers,
        )
        handle_job_run_api_error(resp)
        json_data = resp.json()
        return JobRunResponse(**json_data)

    def cancel_batch_job_run(self, uuid) -> None:
        headers = self.get_auth_header()
        resp = self._requests.delete(
            f"{self.get_resource_url()}/run/batch/{uuid}", headers=headers
        )
        handle_job_run_api_error(resp)
        return

    def cancel_all_job_runs(self, cluster_uuids: Union[List[str], List[UUID]]) -> None:
        headers = self.get_auth_header()
        query_string = build_query_string({"cluster_ids": cluster_uuids})
        resp = self._requests.delete(
            f"{self.get_resource_url()}/runs{query_string}", headers=headers
        )
        handle_job_run_api_error(resp)
        return

    @validate_arguments
    def list_job_runs(
        self,
        type: List[JobRunType] = None,
        batchJobDefinitionUUID: Union[List[UUID], None] = None,
        status: Union[List[JobRunStatus], None] = None,
        clusterUUID: Union[List[UUID], None] = None,
        startedAt: Union[datetime, None] = None,
        finishedAt: Union[datetime, None] = None,
        page: int = DEFAULT_PAGE,
        size: int = DEFAULT_PAGE_SIZE,
        order: PaginationOrder = DEFAULT_ORDER,
    ) -> List[JobRunResponse]:
        args = LIST_QUERY_PARAMS
        query_string_args = {
            k: v for k, v in locals().items() if k in args and v is not None
        }
        headers = self.get_auth_header()
        query_string = build_query_string(query_string_args)
        url = f"{self.get_resource_url()}/run{query_string}"
        resp = self._requests.get(url, headers=headers)

        handle_job_run_api_error(resp)

        result = []
        for json_data in resp.json()["data"]:
            try:
                result.append(JobRunResponse(**json_data))
            except pydantic.ValidationError:
                logging.warning(
                    f"Failed to validate job run response: {json_data['uuid']}"
                )
                result.append(JobRunResponse.construct(**json_data))

        return result

    def get_job_log_links(self, uuid, force_refresh) -> JobRunLogsResponse:
        try:
            headers = self.get_auth_header()
            url = f"{self.get_resource_url('v1')}/runs/{uuid}/logs?forceRefresh={str(force_refresh).lower()}"
            resp = self._requests.get(url, headers=headers)
            handle_job_run_api_error(resp)
            json_data = resp.json()
            job_run_logs_response = JobRunLogsResponse(**json_data)

            def fetch_and_write_file(url: str, file_name: str) -> None:
                try:
                    response = self._requests.get(url)
                    if response.status_code == 200:
                        with open(file_name, "wb") as file:
                            file.write(response.content)
                        print(f"File fetch succeeded to {file_name}")
                    else:
                        logging.error(
                            f"File {file_name} fetch failed: {response.status_code}"
                        )
                except Exception as e:
                    logging.error(f"Bad File fetch Response: {e}")

            fetch_and_write_file(
                job_run_logs_response.stdout_location_url, f"stdout_{uuid}.txt"
            )
            fetch_and_write_file(
                job_run_logs_response.stderr_location_url, f"stderr_{uuid}.txt"
            )
            return job_run_logs_response
        except Exception as e:
            logging.error(f"Bad Response: {e}")
