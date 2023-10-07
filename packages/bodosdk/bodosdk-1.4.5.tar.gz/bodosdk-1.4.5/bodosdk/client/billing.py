from bodosdk.api.billing import BillingApi
from bodosdk.models.base import PaginationOrder
from bodosdk.models.cluster import ClusterPriceExportResponse, ClusterPricingResponse
from bodosdk.models.job import JobRunPriceExportResponse, JobRunPricingResponse
from bodosdk.models.job import (
    DEFAULT_PAGE,
    DEFAULT_PAGE_SIZE,
    DEFAULT_ORDER,
)


class BillingClient:
    def __init__(self, api: BillingApi):
        self._api = api

    def get_cluster_prices(
        self,
        started_at: str = None,
        finished_at: str = None,
        workspace_uuid: str = None,
        page: int = DEFAULT_PAGE,
        size: int = DEFAULT_PAGE_SIZE,
        order: PaginationOrder = DEFAULT_ORDER,
    ) -> ClusterPricingResponse:
        """
        Get cluster prices

        :param started_at:
        :param finished_at:
        :param workspace_uuid:
        :param page:
        :param size:
        :param order:
        :return:
        """
        try:
            return self._api.get_cluster_prices(
                started_at, finished_at, workspace_uuid, page, size, order
            )
        except Exception as exception:
            raise exception

    def get_job_run_prices(
        self,
        started_at: str = None,
        finished_at: str = None,
        workspace_uuid: str = None,
        page: int = DEFAULT_PAGE,
        size: int = DEFAULT_PAGE_SIZE,
        order: PaginationOrder = DEFAULT_ORDER,
    ) -> JobRunPricingResponse:
        """
        Get job run prices

        :param started_at:
        :param finished_at:
        :param workspace_uuid:
        :param page:
        :param size:
        :param order:
        :return:
        """
        try:
            return self._api.get_job_run_prices(
                started_at, finished_at, workspace_uuid, page, size, order
            )
        except Exception as exception:
            raise exception

    def get_cluster_price_export(
        self,
        started_at: str = None,
        finished_at: str = None,
        workspace_uuid: str = None,
    ) -> ClusterPriceExportResponse:
        """
        Get cluster price export
        :param workspace_uuid:
        :param started_at:
        :param finished_at:
        :return:
        """
        try:
            return self._api.get_cluster_price_export(
                started_at, finished_at, workspace_uuid
            )
        except Exception as exception:
            raise exception

    def get_job_run_price_export(
        self,
        started_at: str = None,
        finished_at: str = None,
        workspace_uuid: str = None,
    ) -> JobRunPriceExportResponse:
        """
        Get job run price export

        :param workspace_uuid:
        :param started_at:
        :param finished_at:
        :return:
        """
        try:
            return self._api.get_job_run_price_export(
                started_at, finished_at, workspace_uuid
            )
        except Exception as exception:
            raise exception
