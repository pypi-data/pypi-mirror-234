"""Primary import target for the Python API"""

from mcli.api.cluster import get_clusters
from mcli.api.code_eval import LambdaInput, LambdaResponse, get_code_eval_output
from mcli.api.exceptions import MAPIException
from mcli.api.inference_deployments import (InferenceDeployment, InferenceDeploymentConfig, create_default_deployment,
                                            create_inference_deployment, delete_inference_deployments,
                                            get_inference_deployment, get_inference_deployment_logs,
                                            get_inference_deployments, ping, predict, update_inference_deployment,
                                            update_inference_deployments)
from mcli.api.runs import (FinalRunConfig, Run, RunConfig, RunStatus, create_run, delete_run, delete_runs,
                           follow_run_logs, get_run, get_run_logs, get_runs, start_run, start_runs, stop_run, stop_runs,
                           update_run, update_run_metadata, wait_for_run_status, watch_run_status)
from mcli.api.secrets import create_secret, delete_secrets, get_secrets
from mcli.cli.m_init.m_init import initialize
from mcli.cli.m_set_unset.api_key import set_api_key
from mcli.config import FeatureFlag, MCLIConfig

__all__ = [
    'get_clusters',
    'MAPIException',
    'InferenceDeployment',
    'InferenceDeploymentConfig',
    'create_default_deployment',
    'create_inference_deployment',
    'delete_inference_deployments',
    'get_inference_deployment_logs',
    'get_inference_deployments',
    'get_inference_deployment',
    'ping',
    'predict',
    'FinalRunConfig',
    'Run',
    'RunConfig',
    'RunStatus',
    'create_run',
    'delete_run',
    'delete_runs',
    'follow_run_logs',
    'get_run',
    'get_run_logs',
    'get_runs',
    'start_run',
    'start_runs',
    'stop_run',
    'stop_runs',
    'update_inference_deployment',
    'update_inference_deployments',
    'update_run_metadata',
    'update_run',
    'wait_for_run_status',
    'watch_run_status',
    'create_secret',
    'delete_secrets',
    'get_secrets',
    'initialize',
    'set_api_key',
    'FeatureFlag',
    'MCLIConfig',
    'LambdaInput',
    'LambdaResponse',
    'get_code_eval_output',
]
