""" MCLI Abstraction for Clusters and Utilization """
from __future__ import annotations

import functools
import logging
from dataclasses import dataclass, field
from datetime import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Set

from dateutil import parser

from mcli.api.exceptions import MAPIException
from mcli.api.schema.generic_model import DeserializableModel, convert_datetime
from mcli.models.run_config import SchedulingConfig, SchedulingTranslation
from mcli.utils.utils_model import SubmissionType

logger = logging.getLogger(__name__)


def check_response(response: Dict[str, Any], expected: Set[str]) -> None:
    missing = expected - set(response)
    if missing:
        raise MAPIException(HTTPStatus.INTERNAL_SERVER_ERROR, f'Missing fields in response: {", ".join(missing)}')


@dataclass
class ClusterUtilizationByDeployment:
    """Utilization for a specific run on a cluster
    """

    id: str
    user: str
    name: str
    gpu_num: int
    instance: str
    created_at: datetime
    scheduling: SchedulingConfig = field(default_factory=SchedulingConfig)  # Never used. Only for linting

    @property
    def display_name(self) -> str:
        return self.name

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> ClusterUtilizationByDeployment:
        check_response(response, {'id', 'userName', 'deploymentName', 'gpuNum', 'createdAt', 'instance'})
        return cls(id=response['id'],
                   user=response['userName'],
                   name=response['deploymentName'],
                   gpu_num=response['gpuNum'],
                   instance=response['instance'],
                   created_at=parser.parse(response['createdAt']))


@dataclass
class ClusterUtilizationByRun:
    """Utilization for a specific run on a cluster
    """

    id: str
    user: str
    name: str
    run_name: str  # DEPRECATE
    gpu_num: int
    instance: str
    created_at: datetime
    scheduling: SchedulingConfig
    reason: str
    estimated_end_time: Optional[datetime] = None
    max_duration_seconds: Optional[int] = None
    start_time: Optional[datetime] = None
    gpu_type: Optional[str] = None

    @property
    def display_name(self) -> str:
        if self.scheduling.get('retry_on_system_failure'):
            return f'{self.name} 🐕'

        return self.name

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> ClusterUtilizationByRun:
        check_response(response, {'id', 'userName', 'runName', 'gpuNum', 'createdAt', 'instance'})
        estimated_end_time = response.get('estimatedEndTime', None)
        eta = convert_datetime(estimated_end_time) if estimated_end_time else None
        start_time = response.get("startTime", None)
        start = convert_datetime(start_time) if start_time else None

        return cls(
            id=response['id'],
            user=response['userName'],
            run_name=response['runName'],
            name=response['runName'],
            gpu_num=response['gpuNum'],
            gpu_type=response['gpuType'] if 'gpuType' in response else None,
            instance=response['instance'],
            created_at=parser.parse(response['createdAt']),
            estimated_end_time=eta,
            scheduling=SchedulingTranslation.from_mapi(response.get('scheduling', {})),
            max_duration_seconds=response.get("maxDurationSeconds", None),
            start_time=start,
            reason=response.get('reason', ''),
        )


@dataclass
class InstanceUtilization:
    """Utilization on a cluster instance
    """
    instance: Instance
    cluster_id: str  # TODO: Deprecate
    name: str  # TODO: Deprecate
    gpu_type: str  # TODO: Deprecate and pull gpu_type from `instance`
    gpus_per_node: int  # TODO: Deprecate and pull gpus_per_node from `instance`
    num_nodes: int  # TODO: Deprecate and pull from `instance`
    gpus_used: int
    gpus_available: int
    gpus_total: int

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> InstanceUtilization:
        check_response(response, {'clusterId', 'instance', 'gpusUsed', 'gpusAvailable', 'gpusTotal'})
        instance = Instance.from_mapi_response(response['instance'])
        return cls(
            instance=instance,
            cluster_id=response['clusterId'],
            name=instance.name,
            gpu_type=instance.gpu_type,
            gpus_per_node=instance.gpus,
            num_nodes=instance.nodes,
            gpus_used=response['gpusUsed'],
            gpus_available=response['gpusAvailable'],
            gpus_total=response['gpusTotal'],
        )

    def __gt__(self, other: InstanceUtilization):
        return self.gpus_available == 0 or self.name > other.name


@dataclass
class ClusterUtilization:
    """Utilization on a cluster
    """
    anonymize_users: bool  # TODO: Deprecate
    cluster_instance_utils: List[InstanceUtilization] = field(default_factory=list)
    active_by_user: List[ClusterUtilizationByRun] = field(default_factory=list)  # DEPRECATE
    queued_by_user: List[ClusterUtilizationByRun] = field(default_factory=list)  # DEPRECATE
    active_runs_by_user: List[ClusterUtilizationByRun] = field(default_factory=list)
    queued_runs_by_user: List[ClusterUtilizationByRun] = field(default_factory=list)
    active_deployments_by_user: List[ClusterUtilizationByDeployment] = field(default_factory=list)
    queued_deployments_by_user: List[ClusterUtilizationByDeployment] = field(default_factory=list)

    def get_submissions(self, submission_type: SubmissionType, is_active: bool):
        if submission_type is SubmissionType.TRAINING:
            return self.active_by_user if is_active else self.queued_by_user
        else:
            return self.active_deployments_by_user if is_active else self.queued_deployments_by_user

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> ClusterUtilization:
        check_response(
            response, {
                'instanceUtils', 'activeRunsByUser', 'queuedRunsByUser', 'activeDeploymentsByUser',
                'queuedDeploymentsByUser', 'anonymizeUsers'
            })
        return cls(
            cluster_instance_utils=sorted(
                [InstanceUtilization.from_mapi_response(i) for i in response['instanceUtils']]),
            active_by_user=[ClusterUtilizationByRun.from_mapi_response(i) for i in response['activeRunsByUser']],
            queued_by_user=[ClusterUtilizationByRun.from_mapi_response(i) for i in response['queuedRunsByUser']],
            active_runs_by_user=[ClusterUtilizationByRun.from_mapi_response(i) for i in response['activeRunsByUser']],
            queued_runs_by_user=[ClusterUtilizationByRun.from_mapi_response(i) for i in response['queuedRunsByUser']],
            active_deployments_by_user=[
                ClusterUtilizationByDeployment.from_mapi_response(i) for i in response['activeDeploymentsByUser']
            ],
            queued_deployments_by_user=[
                ClusterUtilizationByDeployment.from_mapi_response(i) for i in response['queuedDeploymentsByUser']
            ],
            anonymize_users=response['anonymizeUsers'])


@dataclass
class Node:
    """Node on an instance for a cluster
    """
    name: str
    is_alive: bool
    is_schedulable: bool

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> Node:
        check_response(response, {'name', 'isAlive', 'isSchedulable'})
        return cls(name=response['name'], is_alive=response['isAlive'], is_schedulable=response['isSchedulable'])


@dataclass
@functools.total_ordering
class Instance:
    """Instance of a cluster
    """
    name: str
    gpu_type: str
    gpus: int
    cpus: Optional[int]
    memory: str
    storage: str
    nodes: int
    # TODO: Deprecate, no longer used
    gpu_nums: List[int] = field(default_factory=list)
    node_details: List[Node] = field(default_factory=list)

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> Instance:
        check_response(response, {'name', 'gpusPerNode', 'numNodes', 'gpuType', 'nodes'})
        return cls(
            name=response['name'],
            gpu_type=response['gpuType'],
            gpus=response['gpusPerNode'],
            cpus=response['cpus'] if 'cpus' in response else None,
            memory=response['memory'] if 'memory' in response else '',
            storage=response['storage'] if 'storage' in response else '',
            nodes=response['numNodes'],
            gpu_nums=response['gpuNums'] if 'gpuNums' in response else [],
            node_details=[Node.from_mapi_response(i) for i in response.get('nodes', [])],
        )

    def __lt__(self, other: Instance):
        if self.gpu_type.lower() == 'none':
            return True
        return self.gpu_type < other.gpu_type


def get_provider_name(raw_provider: str):
    raw_provider = raw_provider.upper()

    overrides = {
        'COREWEAVE': 'CoreWeave',
        'MICROK8S': 'MicroK8s',
        'MOSAICML_COLO': 'MosaicML',
    }

    return overrides.get(raw_provider, raw_provider.capitalize())


@dataclass
@functools.total_ordering
class ClusterDetails(DeserializableModel):
    """Details of a cluster, including instances and utilization
    """

    name: str
    provider: str = 'MosaicML'
    allow_fractional: bool = False
    allow_multinode: bool = False
    cluster_instances: List[Instance] = field(default_factory=list)
    submission_type: Optional[SubmissionType] = None  # TODO: deprecate
    submission_types: List[SubmissionType] = field(default_factory=list)
    is_multitenant: bool = False
    scheduler_enabled: bool = False
    utilization: Optional[ClusterUtilization] = None

    kubernetes_context: str = ''  # TODO: deprecate
    namespace: str = ''  # TODO: deprecate

    id: Optional[str] = None

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> ClusterDetails:
        check_response(response, {'name'})
        utilization = None if 'utilization' not in response else ClusterUtilization.from_mapi_response(
            response['utilization'])
        submission_types = [SubmissionType.from_mapi(type) for type in response.get('allowedSubmissionTypes', [])]
        return cls(name=response['name'],
                   provider=get_provider_name(response.get('provider', '')),
                   allow_fractional=response.get('allowFractional', False),
                   allow_multinode=response.get('allowMultinode', False),
                   cluster_instances=[Instance.from_mapi_response(i) for i in response.get('allowedInstances', [])],
                   submission_type=submission_types[0] if submission_types else None,
                   submission_types=submission_types,
                   is_multitenant=response.get('isMultiTenant', False),
                   scheduler_enabled=response.get('schedulerEnabled', False),
                   utilization=utilization,
                   id=response.get('id'))

    def __lt__(self, other: ClusterDetails):
        return self.name < other.name
