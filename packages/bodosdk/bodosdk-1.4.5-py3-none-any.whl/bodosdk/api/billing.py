from bodosdk.api.base import BackendApi
from pydantic import validate_arguments
from bodosdk.exc import (
    ConflictException,
    ResourceNotFound,
    ServiceUnavailable,
    UnknownError,
    ValidationError,
)
from bodosdk.models.base import PaginationOrder
from bodosdk.models.cluster import ClusterPriceExportResponse, ClusterPricingResponse
from bodosdk.models.job import JobRunPriceExportResponse, JobRunPricingResponse
from bodosdk.models.job import (
    DEFAULT_PAGE,
    DEFAULT_PAGE_SIZE,
    DEFAULT_ORDER,
)


def handle_billing_api_error(resp):
    status_code = resp.status_code
    if str(status_code).startswith("2"):
        return
    print_message = False
    error_message = None
    if "message" in resp.json():
        print_message = True
        error_message = resp.json()["message"]
        error_message += f" status code: {str(status_code)}"

    if str(status_code).startswith("5"):
        raise ServiceUnavailable(
            error_message
            if print_message
            else f"Could not Complete Request: {str(status_code)}"
        )
    if status_code == 404:
        raise ResourceNotFound(
            error_message
            if print_message
            else f"Resource Not Found: {str(status_code)}"
        )
    if status_code == 409:
        raise ConflictException(
            error_message
            if print_message
            else f"request could not be processed because of conflict in the request: {str(status_code)}"
        )

    if status_code == 400:
        raise ValidationError(
            error_message if print_message else f"Bad request: {str(status_code)}"
        )
    # if none of these work
    raise UnknownError(
        error_message
        if print_message
        else f"Encountered Unexpected Error: {str(status_code)}"
    )


class BillingApi(BackendApi):
    def __init__(self, *args, **kwargs):
        super(BillingApi, self).__init__(*args, **kwargs)

    @validate_arguments
    def get_cluster_prices(
        self,
        started_at: str = None,
        finished_at: str = None,
        workspace_uuid: str = None,
        page: int = DEFAULT_PAGE,
        size: int = DEFAULT_PAGE_SIZE,
        order: PaginationOrder = DEFAULT_ORDER,
    ):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.get(
            f"{self.get_resource_url()}/metering/pricing?startedAt={started_at}"
            f"&finishedAt={finished_at}&workspaceUUID={workspace_uuid}"
            f"&page={page}&size={size}&order={order.value}",
            headers=headers,
        )
        handle_billing_api_error(resp)
        return ClusterPricingResponse(**resp.json())

    @validate_arguments
    def get_job_run_prices(
        self,
        started_at: str = None,
        finished_at: str = None,
        workspace_uuid: str = None,
        page: int = DEFAULT_PAGE,
        size: int = DEFAULT_PAGE_SIZE,
        order: PaginationOrder = DEFAULT_ORDER,
    ):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.get(
            f"{self.get_resource_url()}/job/runs/pricing?startedAt={started_at}"
            f"&finishedAt={finished_at}&workspaceUUID={workspace_uuid}"
            f"&page={page}&size={size}&order={order.value}",
            headers=headers,
        )
        handle_billing_api_error(resp)
        return JobRunPricingResponse(**resp.json())

    @validate_arguments
    def get_cluster_price_export(
        self,
        started_at: str = None,
        finished_at: str = None,
        workspace_uuid: str = None,
    ):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.get(
            f"{self.get_resource_url()}/metering/price-export?startedAt={started_at}"
            f"&finishedAt={finished_at}&workspaceUUID={workspace_uuid}",
            headers=headers,
        )
        handle_billing_api_error(resp)
        return ClusterPriceExportResponse(**resp.json())

    @validate_arguments
    def get_job_run_price_export(
        self,
        started_at: str = None,
        finished_at: str = None,
        workspace_uuid: str = None,
    ):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.get(
            f"{self.get_resource_url()}/job/runs/price-export?startedAt={started_at}"
            f"&finishedAt={finished_at}&workspaceUUID={workspace_uuid}",
            headers=headers,
        )
        handle_billing_api_error(resp)
        return JobRunPriceExportResponse(**resp.json())
