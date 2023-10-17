""" Run Input """
from __future__ import annotations

import copy
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from http import HTTPStatus
from typing import Any, Dict, Generic, List, Optional, Sequence, TypeVar

import yaml
from typing_extensions import TypedDict

from mcli.api.exceptions import MAPIException, MCLIRunConfigValidationError
from mcli.api.schema.generic_model import DeserializableModel
from mcli.utils.utils_config import BaseSubmissionConfig, ComputeConfig, ComputeTranslation, strip_nones
from mcli.utils.utils_string_functions import (camel_case_to_snake_case, clean_run_name, snake_case_to_camel_case,
                                               validate_image)

logger = logging.getLogger(__name__)


class SchedulingConfig(TypedDict, total=False):
    """Typed dictionary for nested scheduling configurations"""
    priority: Optional[str]
    resumable: Optional[bool]  # TODO: deprecate resumable
    preemptible: Optional[bool]
    retryOnSystemFailure: Optional[bool]
    max_retries: Optional[int]
    retry_on_system_failure: Optional[bool]
    max_duration: Optional[float]


@dataclass
class FinalRunConfig(DeserializableModel):
    """A finalized run configuration

    This configuration must be complete, with enough details to submit a new run to the
    MosaicML platform.
    """

    cpus: int
    integrations: List[Dict[str, Any]]
    env_variables: List[Dict[str, str]]

    parameters: Dict[str, Any]

    image: Optional[str] = None
    name: Optional[str] = None
    parent_name: Optional[str] = None

    # deprecating in favor of compute['gpu_type']
    gpu_type: Optional[str] = None
    gpu_num: Optional[int] = None  # deprecating in favor of compute['gpus']
    optimization_level: int = 0  # deprecated
    run_id: str = ''  # deprecated, id calculated by mapi

    # Make both optional for initial rollout
    # Eventually make entrypoint required and deprecate command
    command: str = ''
    entrypoint: str = ''

    # Platform is deprecated, but not required for backwards compatibility
    cluster: str = ''
    platform: str = ''

    # Partition is an optional new keyword
    partitions: Optional[List[str]] = None

    # Scheduling parameters - optional for backwards-compatibility
    scheduling: SchedulingConfig = field(default_factory=SchedulingConfig)

    # Compute parameters - optional for backwards-compatibility
    compute: ComputeConfig = field(default_factory=ComputeConfig)

    # User defined metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    _property_translations = {
        'runName': 'name',
        'parentName': 'parent_name',
        'gpuType': 'gpu_type',
        'gpuNum': 'gpu_num',
        'cpus': 'cpus',
        'cluster': 'cluster',
        'image': 'image',
        'integrations': 'integrations',
        'envVariables': 'env_variables',
        'parameters': 'parameters',
        'command': 'command',
        'entrypoint': 'entrypoint',
        'scheduling': 'scheduling',
        'compute': 'compute',
        'metadata': 'metadata',
    }

    _optional_properties = {
        'parentName',
        'partitions',
        'scheduling',
        'compute',
        'metadata',
    }

    def __str__(self) -> str:
        return yaml.safe_dump(asdict(self))

    def __post_init__(self):
        self.cluster = self.cluster or self.platform

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> FinalRunConfig:
        missing = set(cls._property_translations) - \
            set(response) - cls._optional_properties
        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message=
                f'Missing required key(s) in response to deserialize FinalRunConfig object: {", ".join(missing)}',
            )
        data = {}
        for k, v in cls._property_translations.items():
            if k not in response:
                # This must be an optional property, so skip
                continue
            value = response[k]
            if v == 'env_variables':
                value = EnvVarTranslation.from_mapi(value)
            elif v == 'integrations':
                value = IntegrationTranslation.from_mapi(value)
            elif v == 'scheduling':
                value = SchedulingTranslation.from_mapi(value)
            elif v == 'compute':
                value = ComputeTranslation.from_mapi(value)
            data[v] = value

        return cls(**data)

    @classmethod
    def finalize_config(cls, run_config: RunConfig) -> FinalRunConfig:  # pylint: disable=too-many-statements
        """Create a :class:`~mcli.models.run_config.FinalRunConfig` from the provided
        :class:`~mcli.models.run_config.RunConfig`.

        If the :class:`~mcli.models.run_config.RunConfig` is not fully populated then
        this function fails with an error.

        Args:
            run_config (:class:`~mcli.models.run_config.RunConfig`): The RunConfig to finalize

        Returns:
            :class:`~mcli.models.run_config.FinalRunConfig`: The object created using values from the input

        Raises:
            :class:`~mcli.api.exceptions.MCLIConfigError`: If MCLI config is not present or is missing information
            :class:`~mcli.api.exceptions.MCLIRunConfigValidationError`: If run_config is not valid
        """
        if run_config.cpus is None:
            run_config.cpus = 0

        if run_config.partitions is not None:
            # Validate provided partition is a list of strings
            if not isinstance(run_config.partitions, Sequence):
                run_config.partitions = [str(run_config.partitions)]
            else:
                run_config.partitions = [str(p) for p in run_config.partitions]

        model_as_dict = asdict(run_config)

        # Remove deprecated run_name
        model_as_dict.pop('run_name', None)

        # Remove deprecated platform
        model_as_dict.pop('platform', None)
        model_as_dict = strip_nones(model_as_dict)

        # Fill in default initial values for FinalRunConfig
        if 'name' in model_as_dict:
            model_as_dict['name'] = clean_run_name(model_as_dict.get('name'))

        if isinstance(model_as_dict.get('gpu_type'), int):
            model_as_dict['gpu_type'] = str(model_as_dict['gpu_type'])

        image = model_as_dict.get('image')
        if not image:
            raise MCLIRunConfigValidationError('An image name must be provided using the keyword [bold]image[/]')
        elif not validate_image(image):
            raise MCLIRunConfigValidationError(f'The image name "{model_as_dict["image"]}" is not valid')

        return cls(**model_as_dict)

    def get_parent_name_from_env(self) -> Optional[str]:
        """Get the parent name from the environment

        Returns:
            Optional[str]: The parent name if it exists, otherwise None
        """
        inside_run = os.environ.get('MOSAICML_PLATFORM', 'false').lower() == 'true'
        if not inside_run:
            return None

        return os.environ.get('RUN_NAME')

    def to_create_run_api_input(self) -> Dict[str, Dict[str, Any]]:
        """Convert a run configuration to a proper JSON to pass to MAPI's createRun

        Returns:
            Dict[str, Dict[str, Any]]: The run configuration as a MAPI runInput JSON
        """
        translations = {v: k for k, v in self._property_translations.items()}

        translated_input = {}
        for field_name, value in asdict(self).items():
            if value is None:
                continue
            translated_name = translations.get(field_name, field_name)
            if field_name == 'env_variables':
                value = EnvVarTranslation.to_mapi(value)
            elif field_name == 'integrations':
                value = IntegrationTranslation.to_mapi(value)
            elif field_name == "scheduling":
                value = SchedulingTranslation.to_mapi(value)
            elif field_name == "compute":
                value = ComputeTranslation.to_mapi(value)
            elif field_name == "parameters":
                # parameters should be passed as-is, explicitly
                pass
            elif field_name == "gpu_type" and not value:
                continue
            elif field_name == "cluster" and not value:
                continue
            elif field_name == "platform":
                continue
            elif field_name == "optimization_level":
                continue
            elif isinstance(value, dict):
                value = strip_nones(value)

            translated_input[translated_name] = value

        # Automatically set the parentName if mcli is running inside a run
        if not translated_input.get('parentName'):
            translated_input['parentName'] = self.get_parent_name_from_env()

        return {
            'runInput': translated_input,
        }


T = TypeVar('T')  # pylint: disable=invalid-name
U = TypeVar('U')


class Translation(ABC, Generic[T, U]):
    """ABC for MAPI/MCLI translations"""

    @classmethod
    @abstractmethod
    def to_mapi(cls, value: T) -> U:
        ...

    @classmethod
    @abstractmethod
    def from_mapi(cls, value: U) -> T:
        ...


class EnvVarTranslation(Translation[List[Dict[str, str]], List[Dict[str, str]]]):
    """Translate environment variable configs"""

    MAPI_KEY = 'envKey'
    MAPI_VALUE = 'envValue'

    MCLI_KEY = 'key'
    MCLI_VALUE = 'value'

    @classmethod
    def to_mapi(cls, value: List[Dict[str, str]]) -> List[Dict[str, str]]:
        env_vars = []
        for env_var in value:
            try:
                key = env_var[cls.MCLI_KEY]
                val = env_var[cls.MCLI_VALUE]
            except KeyError as e:
                raise KeyError('Environment variables should be specified as a list '
                               f'of dictionaries with keys: "{cls.MCLI_KEY}" and "{cls.MCLI_VALUE}". '
                               f'Got: {", ".join(list(env_var.keys()))}') from e

            env_vars.append({cls.MAPI_KEY: key, cls.MAPI_VALUE: val})
        return env_vars

    @classmethod
    def from_mapi(cls, value: List[Dict[str, str]]) -> List[Dict[str, str]]:
        env_vars = []
        for env_var in value:
            try:
                key = env_var[cls.MAPI_KEY]
                val = env_var[cls.MAPI_VALUE]
            except KeyError:
                logger.warning(f'Received incompatible environment variable: {env_var}')
                continue
            env_vars.append({cls.MCLI_KEY: key, cls.MCLI_VALUE: val})
        return env_vars


class IntegrationTranslation(Translation[List[Dict[str, Any]], List[Dict[str, Any]]]):
    """Translate integration configs"""

    MAPI_TYPE = 'type'
    MAPI_PARAMS = 'params'

    MCLI_TYPE = 'integration_type'

    @classmethod
    def to_mapi(cls, value: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        value = copy.deepcopy(value)
        integrations_list = []
        for integration in value:
            integration_type = integration.pop(cls.MCLI_TYPE)

            translated_integration = {}
            for param, val in integration.items():
                # Translate keys to camel case for MAPI parameters
                translated_key = snake_case_to_camel_case(param)
                translated_integration[translated_key] = val

            integrations_dict = {cls.MAPI_TYPE: integration_type, cls.MAPI_PARAMS: translated_integration}
            integrations_list.append(integrations_dict)
        return integrations_list

    @classmethod
    def from_mapi(cls, value: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        integrations_list = []
        for integration in value:
            translated_integration = {cls.MCLI_TYPE: integration[cls.MAPI_TYPE]}
            params = integration.get(cls.MAPI_PARAMS, {})
            for param, val in params.items():
                # Translate keys to camel case for MAPI parameters
                translated_key = camel_case_to_snake_case(param)
                translated_integration[translated_key] = val

            integrations_list.append(translated_integration)
        return integrations_list


class SchedulingTranslation(Translation[SchedulingConfig, Dict[str, Any]]):
    """Translate scheduling configs to and from MAPI"""

    translations = {
        "maxRetries": "max_retries",
        "retryOnSystemFailure": "retry_on_system_failure",
        "maxDuration": "max_duration"
    }

    @classmethod
    def from_mapi(cls, value: Dict[str, Any]) -> SchedulingConfig:
        extracted = SchedulingConfig(**{cls.translations.get(k, k): v for k, v in value.items() if k != "priorityInt"})
        return extracted

    @classmethod
    def to_mapi(cls, value: SchedulingConfig) -> Dict[str, Any]:
        inv = {v: k for k, v in cls.translations.items()}
        processed = {inv.get(k, k): v for k, v in value.items() if v is not None}
        return processed


@dataclass
class RunConfig(BaseSubmissionConfig):
    """A run configuration for the MosaicML platform

    Values in here are not yet validated and some required values may be missing.
    On attempting to create the run, a bad config will raise a MapiException with a 400 status code.

    Required args:
        - name (`str`): User-defined name of the run
        - image (`str`): Docker image (e.g. `mosaicml/composer`)
        - command (`str`): Command to use when a run starts
        - compute (:class:`~mcli.ComputeConfig` or `Dict[str, Any]`): Compute configuration. Typically
            a subset of the following fields will be required:

            - `cluster` (`str`): Name of cluster to use
            - `instance` (`str`): Name of instance to use
            - `gpu_type` (`str`): Name of gpu type to use
            - `gpus` (`int`): Number of GPUs to use
            - `cpus` (`int`): Number of CPUs to use
            - `nodes` (`int`): Number of nodes to use

            See `mcli get clusters` for a list of available clusters and instances
    
    Optional args:
        - parameters (`Dict[str, Any]`): Parameters to mount into the environment
        - scheduling (:class:`~mcli.SchedulingConfig` or `Dict[str, Any]`): Scheduling configuration
            - `priority` (`str`): Priority of the run
            - `preemptible` (`bool`): Whether the run is preemptible (default False)
            - `retry_on_system_failure` (`bool`): Whether the run should be retried on system failure (default False)
            - `max_retries` (`int`): Maximum number of retries (default 0)
            - `max_duration` (`float`): Maximum duration of the run in hours (default None)
                Run will be automatically stopped after this duration has elapsed.
        - integrations (`List[Dict[str, Any]]`): List of integrations. See integration documentation for more details:
            https://docs.mosaicml.com/projects/mcli/en/latest/resources/integrations/index.html
        - env_variables (`List[Dict[str, str]]`): List of environment variables. Each `dict` should have:
            - key (`str`): Name of the environment variable
            - value (`str`): Value of the environment variable
        - metadata (`Dict[str, Any]`): Arbitrary metadata to attach to the run
    """
    name: Optional[str] = None
    parent_name: Optional[str] = None
    image: Optional[str] = None
    gpu_type: Optional[str] = None
    gpu_num: Optional[int] = None
    cpus: Optional[int] = None
    cluster: Optional[str] = None
    scheduling: SchedulingConfig = field(default_factory=SchedulingConfig)
    compute: ComputeConfig = field(default_factory=ComputeConfig)
    parameters: Dict[str, Any] = field(default_factory=dict)
    scheduling: SchedulingConfig = field(default_factory=SchedulingConfig)
    integrations: List[Dict[str, Any]] = field(default_factory=list)
    env_variables: List[Dict[str, str]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    command: str = ''
    parameters: Dict[str, Any] = field(default_factory=dict)

    # Deprecated fields
    run_name: Optional[str] = None
    entrypoint: str = ''
    partitions: Optional[List[str]] = None
    optimization_level: Optional[int] = None
    platform: Optional[str] = None

    _property_translations = {
        'runName': 'name',
        'parentName': 'parent_name',
        'gpuNum': 'gpu_num',
        'cpus': 'cpus',
        'cluster': 'cluster',
        'image': 'image',
        'integrations': 'integrations',
        'envVariables': 'env_variables',
        'parameters': 'parameters',
        'command': 'command',
        'entrypoint': 'entrypoint',
        'scheduling': 'scheduling',
        'metadata': 'metadata',
        'compute': 'compute',
    }

    _required_display_properties = {'name', 'image', 'command'}

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> RunConfig:
        data = {}
        for k, v in cls._property_translations.items():
            if k not in response:
                # This must be an optional property, so skip
                continue
            value = response[k]
            if v == 'env_variables':
                value = EnvVarTranslation.from_mapi(value)
            elif v == 'integrations':
                value = IntegrationTranslation.from_mapi(value)
            elif v == 'scheduling':
                value = SchedulingTranslation.from_mapi(value)
            elif v == 'compute':
                value = ComputeConfig(**value)
            data[v] = value

        return cls(**data)

    def __post_init__(self):
        self.name = self.name or self.run_name
        if self.run_name is not None:
            logger.debug('Field "run_name" is deprecated. Please use "name" instead')

        self.cluster = self.cluster or self.platform
        if self.platform is not None:
            logger.debug('Field "platform" is deprecated. Please use "cluster" instead')
