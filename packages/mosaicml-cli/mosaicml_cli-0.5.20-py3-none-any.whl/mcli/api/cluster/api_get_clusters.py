"""get_clusters SDK for MAPI"""
from __future__ import annotations

from concurrent.futures import Future
from http import HTTPStatus
from typing import List, Optional, Union, cast, overload

from typing_extensions import Literal

from mcli.api.engine.engine import convert_plural_future_to_singleton, get_return_response, run_plural_mapi_request
from mcli.api.exceptions import MAPIException
from mcli.api.model.cluster_details import ClusterDetails
from mcli.config import MCLIConfig
from mcli.models.mcli_cluster import Cluster
from mcli.utils.utils_model import SubmissionType

__all__ = ['get_cluster', 'get_clusters']

QUERY_FUNCTION = 'getClusters'
VARIABLE_DATA_NAME = 'getClustersData'
QUERY = f"""
query GetClusters(${VARIABLE_DATA_NAME}: GetClustersInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
    id
    name
    provider
    allowFractional
    allowMultinode
    allowedSubmissionTypes
    isMultiTenant
    schedulerEnabled
    allowedInstances {{
      name
      gpuType
      gpusPerNode
      cpus
      memory
      storage
      gpuNums
      numNodes
      nodes {{
        name
        isAlive
        isSchedulable
        upTime {{
          endDate
          startDate
        }}
      }}
    }}
  }}
}}"""
QUERY_UTILIZATION = f"""
query GetClusters(${VARIABLE_DATA_NAME}: GetClustersInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
    id
    name
    provider
    allowedSubmissionTypes
    isMultiTenant
    schedulerEnabled
    utilization {{
      instanceUtils {{
        instance {{
          name
          gpuType
          gpuNums
          gpusPerNode
          cpus
          memory
          storage
          numNodes
          nodes {{
            name
            isAlive
            isSchedulable
            upTime {{
              endDate
              startDate
            }}
          }}
        }}
        clusterId
        gpusUsed
        gpusAvailable
        gpusTotal
      }}
      activeRunsByUser{{
        id
        createdAt
        userName
        runName
        instance
        gpuNum
        estimatedEndTime
        maxDurationSeconds
        startTime
        scheduling {{
          priority
          retryOnSystemFailure
          preemptible
        }}
      }}
      queuedRunsByUser{{
        id
        createdAt
        userName
        runName
        instance
        gpuNum
        reason
        scheduling {{
          priority
          retryOnSystemFailure
          preemptible
        }}
      }}
      activeDeploymentsByUser{{
        id
        createdAt
        userName
        deploymentName
        instance
        gpuNum
      }}
      queuedDeploymentsByUser{{
        id
        createdAt
        userName
        deploymentName
        instance
        gpuNum
      }}
      anonymizeUsers
    }}
  }}
}}"""


@overload
def get_cluster(
    cluster: Union[str, ClusterDetails],
    *,
    include_utilization: bool = True,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> ClusterDetails:
    ...


@overload
def get_cluster(
    cluster: Union[str, ClusterDetails],
    *,
    include_utilization: bool = True,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[ClusterDetails]:
    ...


def get_cluster(
    cluster: Union[str, ClusterDetails],
    *,
    include_utilization: bool = True,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Gets a cluster available in the MosaicML platform

    Arguments:
        cluster (:class:`~mcli.api.model.cluster_details.ClusterDetails`):
            :class:`~mcli.api.model.cluster_details.ClusterDetails` object or cluster name
            string to get.
        include_utilization (``bool``): Include information on how the cluster is currently
            being utilized
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the run creation takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`get_cluster` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :class:`~mcli.models.cluster_details.ClusterDetails` output, use
            ``return_value.result()`` with an optional ``timeout`` argument.

    Raises:
        ``MAPIException``: If connecting to MAPI, raised when a MAPI communication error occurs
    """
    clusters = cast(Union[List[str], List[ClusterDetails]], [cluster])
    error_message = f"Cluster {cluster if isinstance(cluster, str) else cluster.name} not found"

    if future:
        res = get_clusters(clusters=clusters, timeout=None, future=True, include_utilization=include_utilization)
        return convert_plural_future_to_singleton(res, error_message)

    res = get_clusters(clusters=clusters, timeout=timeout, future=False, include_utilization=include_utilization)
    if not res:
        raise MAPIException(HTTPStatus.NOT_FOUND, error_message)
    return res[0]


@overload
def get_clusters(
    clusters: Optional[Union[List[str], List[Cluster], List[ClusterDetails]]] = None,
    *,
    include_utilization: bool = False,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
    submission_type_filter: Optional[SubmissionType] = None,
) -> List[ClusterDetails]:
    ...


@overload
def get_clusters(
    clusters: Optional[Union[List[str], List[Cluster], List[ClusterDetails]]] = None,
    *,
    include_utilization: bool = False,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
    submission_type_filter: Optional[SubmissionType] = None,
) -> Future[List[ClusterDetails]]:
    ...


def get_clusters(
    clusters: Optional[Union[List[str], List[Cluster], List[ClusterDetails]]] = None,
    *,
    include_utilization: bool = False,
    timeout: Optional[float] = 10,
    future: bool = False,
    submission_type_filter: Optional[SubmissionType] = None,
):
    """Get clusters available in the MosaicML platform

    Arguments:
        clusters (:class:`~mcli.models.mcli_cluster.Cluster`): List of
            :class:`~mcli.models.mcli_cluster.Cluster` objects or cluster name
            strings to get.
        include_utilization (``bool``): Include information on how the cluster is currently
            being utilized
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the run creation takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`get_clusters` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :class:`~mcli.models.cluster_details.ClusterDetails` output, use
            ``return_value.result()`` with an optional ``timeout`` argument.

    Raises:
        ``MAPIException``: If connecting to MAPI, raised when a MAPI communication error occurs
    """
    filters = {}
    if clusters:
        cluster_names = [c.name if isinstance(c, Cluster) else c for c in clusters]
        filters['name'] = {'in': cluster_names}

    if submission_type_filter:
        filters['allowedSubmissionTypes'] = {'has': submission_type_filter.name}

    variables = {
        VARIABLE_DATA_NAME: {
            'filters': filters
        },
    }

    cfg = MCLIConfig.load_config()
    cfg.update_entity(
        variables[VARIABLE_DATA_NAME],
        # TODO: getClusters needs updates to work well with admin entity filters
        # For now, don't set the user because this will enable the organization entity
        # filter to be applied
        # Note this will exclude clusters granted specifically to a user
        set_user=False,
    )

    response = run_plural_mapi_request(
        query=QUERY_UTILIZATION if include_utilization else QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=ClusterDetails,
        variables=variables,
    )
    return get_return_response(response, future=future, timeout=timeout)
