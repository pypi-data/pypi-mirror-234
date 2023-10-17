""" Finetune config """
import logging
from dataclasses import asdict, dataclass
from http import HTTPStatus
from typing import Any, Dict, List, Optional

import yaml

from mcli.api.exceptions import MAPIException, MCLIConfigError
from mcli.models.finetune_task_type import FinetuneTaskType
from mcli.utils.utils_config import BaseSubmissionConfig, strip_nones
from mcli.utils.utils_logging import WARN
from mcli.utils.utils_string_functions import snake_case_to_camel_case

logger = logging.getLogger(__name__)


@dataclass
class FinetuneConfig(BaseSubmissionConfig):
    """Input for finetuning run

    Args:
        model (str): Model to finetune (e.g. 'mosaicml/mpt-30b')
        task_type (FinetuneTaskType): Task type to finetune on (options are 'INSTRUCTION_FINETUNE' or
            'CONTINUED_PRETRAIN')
        train_data_path (str): HF dataset or remote path to training data
        save_folder (str): Folder to save checkpoints and HF checkpoints, currently must be an s3 or GCP path
        eval_data_path (Optional[str]): HF dataset or remote path to eval data
        custom_weights_path (Optional[str]): Remote location of custom weights to use for finetuning
        training_duration (str): Composer variable for the total number of epochs or tokens to train on
            (e.g. 2ep or 10000tok)
        experiment_trackers (Optional[List[Dict]]): List of experiment trackers to use
        gpu_type (Optional[str]): GPU type to use (e.g. 'a100')
        gpus (Optional[int]): Number of GPUs to use
        learning_rate (Optional[float]): Learning rate to use
        context_length (Optional[int]): Context length of the model. Override only works for MPT model families
    """

    model: str
    train_data_path: str
    save_folder: str
    task_type: Optional[str] = "INSTRUCTION_FINETUNE"
    eval_data_path: Optional[str] = None
    custom_weights_path: Optional[str] = None
    training_duration: Optional[str] = None
    experiment_trackers: Optional[List[Dict]] = None
    learning_rate: Optional[float] = None
    context_length: Optional[int] = None

    _required_properties = {'model', 'train_data_path', 'save_folder'}
    _finetune_properties = {
        'model', 'train_data_path', 'save_folder', 'eval_data_path', 'custom_weights_path', 'training_duration',
        'experiment_trackers', 'learning_rate', 'context_length', 'task_type'
    }

    def __str__(self) -> str:
        return yaml.safe_dump(asdict(self))

    @classmethod
    def validate_dict(cls, dict_to_use: Dict, show_unused_warning: bool = True) -> Dict:
        """Load the config from the provided dictionary.
        """
        config_dict = strip_nones(dict_to_use)
        unused_keys = set(dict_to_use) - cls._finetune_properties
        for key in unused_keys:
            del config_dict[key]
        if {'name', 'image', 'command'}.issubset(unused_keys):
            logger.info(f'{WARN} You specified a name, image, and command. Did you mean to use `mcli run`?')
        missing = cls._required_properties - set(dict_to_use)
        if missing:
            raise MCLIConfigError(f'Missing required fields: {", ".join(missing)}',)
        if len(unused_keys) > 0 and show_unused_warning:
            raise MCLIConfigError(f'Encountered unknown fields in finetuning config: {", ".join(unused_keys)}.')
        if not FinetuneTaskType.validate_task_type(config_dict.get('task_type')):
            raise MAPIException(
                HTTPStatus.INTERNAL_SERVER_ERROR, f'Invalid task_type: {config_dict["task_type"]}, currently '
                f'supported options are: {", ".join([x.value for x in FinetuneTaskType])}')
        return config_dict

    @classmethod
    def from_dict(cls, dict_to_use: Dict[str, Any], show_unused_warning: bool = True):
        """Load the config from the provided dictionary.
        """
        config_dict = cls.validate_dict(dict_to_use, show_unused_warning)
        return cls(**config_dict)

    def to_create_finetune_api_input(self) -> Dict[str, Dict[str, Any]]:
        """Converts the FinetuneConfig object to Compute and Finetune that can be used to create a finetune run
        """
        finetune = {}
        config_dict = strip_nones(self.__dict__)
        for key, val in config_dict.items():
            translated_key = snake_case_to_camel_case(key)
            if key in self._finetune_properties:
                finetune[translated_key] = val

        return {'config': finetune}
