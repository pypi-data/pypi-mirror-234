from typing import Dict, List

from bodosdk.api.base import BackendApi
from bodosdk.exc import (
    ResourceNotFound,
    ServiceUnavailable,
    UnknownError,
    ValidationError,
)
from bodosdk.models.cluster import (
    ClusterDefinition,
    InstanceType,
    InstanceCategory,
    BodoImage,
    ClusterResponse,
    ModifyCluster,
    ScaleCluster,
    ClusterList,
)
from bodosdk.models import TaskInfo
from bodosdk.models.job import JobResponse, JobStatus
from bodosdk.models.base import PaginationOrder


def handle_response_for_cluster_action(response):
    if str(response.status_code).startswith("2"):
        return ClusterResponse(**response.json())
    if response.status_code == 404:
        raise ResourceNotFound()
    if response.status_code in (400, 422):
        raise ValidationError(response.json())
    if str(response.status_code).startswith("5"):
        raise ServiceUnavailable
    raise UnknownError


class ClusterApi(BackendApi):
    def __init__(self, *args, **kwargs):
        super(ClusterApi, self).__init__(*args, **kwargs)
        self._resource_url = "clusters"

    def get_available_instances(self, region) -> Dict[str, InstanceCategory]:
        # TODO: This functionality and endpoint should be moved
        resp = self._requests.get(
            f"{self._base_url}/cluster/availableInstances/{region}",
            headers=self.get_auth_header(),
        )

        result = {}
        for row in resp.json():
            cat = InstanceCategory(name=row.get("label"), instance_types={})
            for opt in row.get("options", []):
                instance_type = InstanceType(**opt.get("label"))
                cat.instance_types[instance_type.name] = instance_type
            result[cat.name] = cat
        return result

    def get_available_images(self, region) -> Dict[str, BodoImage]:
        # TODO: This functionality and endpoint should be moved
        resp = self._requests.get(
            f"{self._base_url}/cluster/availableImages/{region}/worker",
            headers=self.get_auth_header(),
        )
        result = {}
        for row in resp.json():
            for opt in row.get("options"):
                img = BodoImage(
                    image_id=opt["label"]["imageId"],
                    bodo_version=opt["label"]["bodo_version"],
                )
                result[img.bodo_version] = img
        return result

    def get_cluster(self, uuid) -> ClusterResponse:
        response = self._requests.get(
            f"{self.get_resource_url('v1')}/{uuid}", headers=self.get_auth_header()
        )
        if str(response.status_code).startswith("2"):
            return ClusterResponse(**response.json())
        if response.status_code == 404:
            raise ResourceNotFound
        if response.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError(response.content)

    def get_all_clusters(
        self,
        page: int = 1,
        page_size: int = 10,
        order: PaginationOrder = PaginationOrder.ASC,
    ) -> ClusterList:
        response = self._requests.get(
            f"{self.get_resource_url('v2')}",
            headers=self.get_auth_header(),
            params={"page": page, "size": page_size, "order": order},
        )
        if str(response.status_code).startswith("2"):
            return ClusterList(**response.json())
        if response.status_code == 404:
            raise ResourceNotFound
        if response.status_code == 503:
            raise ServiceUnavailable
        raise response.raise_for_status()

    def create_cluster(self, cluster_definition: ClusterDefinition) -> ClusterResponse:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        # TODO: Change endpoint path after we will have new in clusters controller
        resp = self._requests.post(
            f"{self._base_url}/cluster",
            data=cluster_definition.json(by_alias=True),
            headers=headers,
        )
        if str(resp.status_code).startswith("2"):
            return ClusterResponse(**resp.json())
        if resp.status_code == 404:
            raise ResourceNotFound("Probably wrong workspace keys")
        if resp.status_code in (400, 422):
            raise ValidationError(resp.json())
        if resp.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError

    def get_tasks_in_cluster(self, uuid):
        response = self._requests.get(
            f"{self.get_resource_url()}/{uuid}/tasks", headers=self.get_auth_header()
        )
        all_tasks: List[TaskInfo] = []
        for entry in response.json():
            all_tasks.append(TaskInfo(**entry))
        return all_tasks

    def get_jobs_for_cluster(self, uuid, status=[]):
        validated_status = []
        for arg in status:
            if isinstance(arg, str):
                validated_status.append(arg)
            if isinstance(arg, JobStatus):
                validated_status.append(arg.value)
            else:
                raise TypeError("items in status must be of type JobStatus")

        status_str = f"?status={','.join(validated_status)}" if len(status) else ""
        # Note: Old functionality available only in cluster controller
        response = self._requests.get(
            f"{self._base_url}/cluster/{uuid}/jobs{status_str}",
            headers=self.get_auth_header(),
        )

        jobs: List[JobResponse] = []
        for entry in response.json():
            jobs.append(JobResponse(**entry))
        return jobs

    def remove_cluster(self, uuid, force_remove, mark_as_terminated):
        params = {
            "force": str(force_remove).lower(),
            "mark_as_terminated": str(mark_as_terminated).lower(),
        }
        response = self._requests.delete(
            f"{self.get_resource_url('v1')}/{uuid}",
            params=params,
            headers=self.get_auth_header(),
        )
        if str(response.status_code).startswith("2"):
            return
        if response.status_code == 404:
            raise ResourceNotFound
        if response.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError(response.content)

    def scale_cluster(self, scale_cluster: ScaleCluster):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.patch(
            f"{self.get_resource_url('v1')}/{scale_cluster.uuid}",
            data=scale_cluster.json(by_alias=True, exclude={"uuid": True}),
            headers=headers,
        )

        if str(resp.status_code).startswith("2"):
            return ClusterResponse(**resp.json())
        if resp.status_code == 404:
            raise ResourceNotFound()
        if resp.status_code in (400, 422):
            raise ValidationError(resp.json())
        if resp.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError

    def modify_cluster(self, modify_cluster: ModifyCluster):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.patch(
            f"{self.get_resource_url('v1')}/{modify_cluster.uuid}",
            data=modify_cluster.json(by_alias=True, exclude={"uuid": True}),
            headers=headers,
        )
        if str(resp.status_code).startswith("2"):
            return ClusterResponse(**resp.json())
        if resp.status_code == 404:
            raise ResourceNotFound()
        if resp.status_code in (400, 422):
            raise ValidationError(resp.json())
        if resp.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError

    def pause(self, uuid):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.put(
            f"{self.get_resource_url('v1')}/{uuid}/pause", headers=headers
        )
        return handle_response_for_cluster_action(resp)

    def resume(self, uuid):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.put(
            f"{self.get_resource_url('v1')}/{uuid}/resume", headers=headers
        )
        return handle_response_for_cluster_action(resp)

    def stop(self, uuid):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            f"{self.get_resource_url('v1')}/{uuid}/stop", headers=headers
        )
        return handle_response_for_cluster_action(resp)

    def restart(self, uuid):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            f"{self.get_resource_url('v1')}/{uuid}/restart", headers=headers
        )
        return handle_response_for_cluster_action(resp)
