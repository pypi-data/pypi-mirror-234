"""Utils for modifying MCLI Configs"""
import copy
import logging
import random
import string
import warnings
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

import yaml
from typing_extensions import TypedDict

from mcli.utils.utils_logging import WARN, str_presenter
from mcli.utils.utils_string_functions import camel_case_to_snake_case, snake_case_to_camel_case
from mcli.utils.utils_yaml import load_yaml

logger = logging.getLogger(__name__)


class ComputeConfig(TypedDict, total=False):
    """Typed dictionary for nested compute requests"""
    cluster: Optional[str]
    instance: Optional[str]
    nodes: Optional[int]
    gpu_type: Optional[str]
    gpus: Optional[int]
    cpus: Optional[int]


def uuid_generator(length: int = 10) -> str:
    allowed_characters = string.ascii_lowercase + string.digits
    items = random.choices(population=allowed_characters, k=length)
    return ''.join(items)


@dataclass
class BaseSubmissionConfig():
    """ Base class for config objects"""

    _required_display_properties = set()

    @classmethod
    def empty(cls):
        return cls()

    @classmethod
    def from_file(cls, path: Union[str, Path]):
        """Load the config from the provided YAML file.
        Args:
            path (Union[str, Path]): Path to YAML file
        Returns:
            BaseConfig: The BaseConfig object specified in the YAML file
        """
        config = load_yaml(path)
        return cls.from_dict(config, show_unused_warning=True)

    @classmethod
    def from_dict(cls, dict_to_use: Dict[str, Any], show_unused_warning: bool = False):
        """Load the config from the provided dictionary.
        Args:
            dict_to_use (Dict[str, Any]): The dictionary to populate the BaseConfig with
        Returns:
            BaseConfig: The BaseConfig object specified in the dictionary
        """
        field_names = list(map(lambda x: x.name, fields(cls)))

        unused_keys = []
        constructor = {}

        for key, value in dict_to_use.items():
            if key in field_names:
                constructor[key] = value
            else:
                unused_keys.append(key)

        if len(unused_keys) > 0 and show_unused_warning:
            if {'model', 'train_data_path'}.issubset(unused_keys):
                logger.info(
                    f'{WARN} You specified a model, train_data_path, and cluster. Did you mean to use `mcli finetune`?')
            else:
                #pylint: disable=line-too-long
                warnings.warn(
                    f'! Encountered unknown fields {", ".join(unused_keys)} which were not used in creating the request'
                )

        return cls(**constructor)

    def __str__(self) -> str:
        filtered_dict = {}
        for k, v in asdict(self).items():
            # skip nested and direct empty values for optional properties
            if k not in self._required_display_properties:
                if isinstance(v, dict) and not any(v.values()):
                    continue
                if not v:
                    continue
            filtered_dict[k] = v
        # to use with safe_dump:
        yaml.representer.SafeRepresenter.add_representer(str, str_presenter)

        return yaml.safe_dump(filtered_dict, default_flow_style=False, sort_keys=False).strip()


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


class ComputeTranslation(Translation[ComputeConfig, Dict[str, Any]]):
    """Translate compute configs to and from MAPI"""

    translations = {
        "gpuType": "gpu_type",
        "nodeNames": "node_names",
    }

    @classmethod
    def from_mapi(cls, value: Dict[str, Any]) -> ComputeConfig:
        extracted = ComputeConfig(**{cls.translations.get(k, k): v for k, v in value.items()})
        return extracted

    @classmethod
    def to_mapi(cls, value: ComputeConfig) -> Dict[str, Any]:
        inv = {v: k for k, v in cls.translations.items()}
        processed = {inv.get(k, k): v for k, v in value.items() if v is not None}
        return processed


def strip_nones(d: Dict[str, Any]) -> Dict[str, Any]:
    """Remove all keys with None values from a dictionary"""
    return {k: v for k, v in d.items() if v is not None}
