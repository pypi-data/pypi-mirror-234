from typing import Dict, List, Union
from uuid import UUID

from bodosdk.api.cluster import ClusterApi
from bodosdk.models.cluster import (
    ClusterDefinition,
    ClusterResponse,
    InstanceCategory,
    BodoImage,
    ModifyCluster,
    ScaleCluster,
    ClusterList,
)
from bodosdk.models import TaskInfo
from bodosdk.models.job import JobClusterDefinition, JobResponse
from bodosdk.models.base import PaginationOrder, ClusterStatus


class ClusterClient:
    def __init__(self, api: ClusterApi):
        self._api = api

    def get_available_instance_types(self, region: str) -> Dict[str, InstanceCategory]:
        """
        Returns mapping of categorized instance types

        :param region: region for which we check instance types
        :type region: str
        :return: mapping where key is category name
        :rtype: Dict[str, InstanceCategory]
        """
        return self._api.get_available_instances(region)

    def get_available_images(self, region: str) -> Dict[str, BodoImage]:
        """
        Returns mapping of bodo version and image name

        :param region: region for which we check images
        :type region: str
        :return: mapping where key is bodo version and value is object with name and version
        :rtype: Dict[str, BodoImage]
        """
        return self._api.get_available_images(region)

    def get_definition_from_uuid(self, uuid) -> JobClusterDefinition:
        """
        Returns a JobClusterDefinition object that the client can use while defining a JobDefinition
        If a client wants to spin up a new cluster with identical configurations as the one they already have running,
        with `uuid`, call this function to get a JobClusterDefinition they can use to send jobs to the newly
        defined cluster.

        :param uuid: cluster uuid in the bodo platform dashboard
        :type uuid: str
        :return: JobClusterDefinition with metadata: instance type, image id, accelerated networking and workers
        :rtype: JobClusterDefinition
        """
        return JobClusterDefinition(**self._api.get_cluster(uuid).dict())

    def list(
        self,
        page: int = 1,
        page_size: int = 10,
        order: PaginationOrder = PaginationOrder.ASC,
    ) -> ClusterList:
        """
        Return metadata about all the clusters which are currently defined by the client.
        The metadata include name of the cluster, uuid, status and description if any.

        :rtype: ClusterList
        """
        return self._api.get_all_clusters(page, page_size, order)

    def get(self, uuid) -> ClusterResponse:
        """
        Given a uuid for a specific cluster, returns a ClusterResponse object to list out the details about the cluster
        """
        return self._api.get_cluster(uuid)

    def create(self, cluster_definition: ClusterDefinition) -> ClusterResponse:
        """
        Creates a new cluster for the client to use. Takes in a ClusterDefinition object as an input and
        creates a cluster based on the data specified in the objects. Returns a ClusterResponse object in
        case of a success with metadata about the cluster created.

        :param: Details about the new cluster to be created
        :type: ClusterDefinition
        :return: response after creating a cluster
        :rtype: ClusterResponse
        """
        return self._api.create_cluster(cluster_definition)

    def list_tasks(self, uuid) -> List[TaskInfo]:
        """
        Given a uuid of a cluster, returns a list of all tasks running in the cluster. The returned list contains an
        object with details about the uuid, status, type and logs of the task.

        :param: uuid of the cluster to get tasks at
        :type: int
        :return: List of information about tasks running in the cluster. Each element of the list is an object with
                    fields: uuid, status, taskType and logs
        :rtype: List[TaskInfo]
        """
        return self._api.get_tasks_in_cluster(uuid)

    def list_jobs(self, uuid, status=[]) -> List[JobResponse]:
        """
        Given a uuid of a cluster, returns a list of jobs for the cluster.

        :param: uuid of the cluster to get jobs for
        :type: str
        :param: if supplied only jobs with statuses in 'status' are returned
        :type: List[JobStatus]
        :return: List of information about jobs for the cluster.
        :rtype: List[TaskInfo]
        """

        return self._api.get_jobs_for_cluster(uuid, status)

    def remove(
        self,
        uuid: Union[str, UUID],
        force_remove: bool = False,
        mark_as_terminated: bool = False,
    ):
        """
        Removes the cluster with the given uuid.
        Also takes in 2 options: to force delete the cluster and to mark it as permanently terminated.
        """
        return self._api.remove_cluster(uuid, force_remove, mark_as_terminated)

    def scale(self, scale_cluster: ScaleCluster) -> ClusterResponse:
        """
        Changes the number of workers in the cluster with `uuid` to the specified new scale.
        The input `new_scale` is of type ScaleCluster which has an entry for the new number of workers in the cluster
        returns a cluster response object.

        :input: uuid and new scale
        :type: str and ScaleCluster object
        :return: the updates metadata about the cluster after the api call
        :rtype: ClusterResponse
        """
        return self._api.scale_cluster(scale_cluster)

    def modify(self, modify_cluster: ModifyCluster) -> ClusterResponse:
        """
        Allows the client to the edit cluster metadata, which includes the description, auto pause time
        auto stop time and also the number of workers in the cluster with `uuid` to the specified
        new scale, which will trigger a scale task on the cluster

        :input uuid
        :input modify_cluster ModifyCluster object which fields description(string), auto_pause(minutes, int)
                auto_stop(minutes, int) and workers_quantity(int)
        :type: str and ModifyClusteobject
        :return: the updates metadata about the cluster after the api call
        :rtype: ClusterResponse
        """
        return self._api.modify_cluster(modify_cluster)

    def pause(self, uuid) -> ClusterResponse:
        """
        Stops cluster, cluster may be resumed later on.

        :input: uuid
        :type: uuid
        :return: the updates metadata about the cluster after the api call
        :rtype: ClusterResponse
        """
        return self._api.pause(uuid)

    def stop(self, uuid) -> ClusterResponse:
        """
        Stops cluster, cluster may be restarted later on.

        :input: uuid
        :type: uuid
        :return: the updates metadata about the cluster after the api call
        :rtype: ClusterResponse
        """
        cluster_data = self._api.get_cluster(uuid)
        if cluster_data.status == ClusterStatus.SCALING:
            raise Exception("Cluster is scaling, please try again later")
        return self._api.stop(uuid)

    def restart(self, uuid) -> ClusterResponse:
        """
        Restart stopped cluster

        :input: uuid
        :type: uuid
        :return: the updates metadata about the cluster after the api call
        :rtype: ClusterResponse
        """
        return self._api.restart(uuid)

    def resume(self, uuid) -> ClusterResponse:
        """
        Resume paused cluster

        :input: uuid
        :type: uuid
        :return: the updates metadata about the cluster after the api call
        :rtype: ClusterResponse
        """
        return self._api.resume(uuid)
