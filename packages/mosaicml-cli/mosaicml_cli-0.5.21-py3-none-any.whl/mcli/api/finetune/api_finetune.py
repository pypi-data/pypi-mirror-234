"""Finetuning API"""
from __future__ import annotations

from concurrent.futures import Future
from typing import Dict, List, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import get_return_response, run_singular_mapi_request
from mcli.api.runs import Run
from mcli.models.finetune_config import FinetuneConfig

QUERY_FUNCTION = 'createFinetune'
VARIABLE_DATA_NAME = 'createFinetuneData'
# This returns the same data that the create_run function returns
# for consistency when rendering the describe output
QUERY = f"""
mutation CreateFinetune(${VARIABLE_DATA_NAME}: CreateFinetuneInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
    id
    name
    createdByEmail
    status
    createdAt
    startedAt
    completedAt
    updatedAt
    reason
    priority
    maxRetries
    preemptible
    retryOnSystemFailure
    resumptions {{
        clusterName
        cpus
        gpuType
        gpus
        nodes
        executionIndex
        startTime
        endTime
        status
    }}
    details {{
        originalRunInput
        metadata
        lastExecutionId
    }}
  }}
}}"""


@overload
def finetune(model: str,
             train_data_path: str,
             save_folder: str,
             task_type: Optional[str] = "INSTRUCTION_FINETUNE",
             eval_data_path: Optional[str] = None,
             custom_weights_path: Optional[str] = None,
             training_duration: Optional[str] = None,
             learning_rate: Optional[float] = None,
             context_length: Optional[int] = None,
             experiment_trackers: Optional[List[Dict]] = None,
             *,
             timeout: Optional[float] = 10,
             future: Literal[False] = False) -> Run:
    ...


@overload
def finetune(model: str,
             train_data_path: str,
             save_folder: str,
             task_type: Optional[str] = "INSTRUCTION_FINETUNE",
             eval_data_path: Optional[str] = None,
             custom_weights_path: Optional[str] = None,
             training_duration: Optional[str] = None,
             learning_rate: Optional[float] = None,
             context_length: Optional[int] = None,
             experiment_trackers: Optional[List[Dict]] = None,
             *,
             timeout: Optional[float] = 10,
             future: Literal[False] = False) -> Future[Run]:
    ...


def finetune(model: str,
             train_data_path: str,
             save_folder: str,
             task_type: Optional[str] = "INSTRUCTION_FINETUNE",
             eval_data_path: Optional[str] = None,
             custom_weights_path: Optional[str] = None,
             training_duration: Optional[str] = None,
             learning_rate: Optional[float] = None,
             context_length: Optional[int] = None,
             experiment_trackers: Optional[List[Dict]] = None,
             *,
             timeout: Optional[float] = 10,
             future: Literal[False] = False) -> Union[Run, Future[Run]]:
    """Finetunes a model on a finetuning dataset and converts the final composer checkpoint to a
    Hugging Face formatted checkpoint for inference.

    Args:
        model: The name of the Hugging Face model to use. Current available options are 
            ``mosaicml/mpt-7b-8k``, ``mosaicml/mpt-30b``, ``mosaicml/mpt-7b``, ``meta-llama/Llama-2-7b-hf``,
            ``meta-llama/Llama-2-13b-hf`` and ``meta-llama/Llama-2-70b-hf``.
        task_type: The type of finetuning task to run. Current available options are ``INSTRUCTION_FINETUNE``
            and ``CONTINUED_PRETRAIN``, defaults to INSTRUCTION_FINETUNE.
        train_data_path: The full remote location of your training data (eg 's3://my-bucket/my-data.jsonl'). For
            INSTRUCTION_FINETUNE, another option is to provide the name of a Hugging Face dataset that includes the
            train split, like 'mosaicml/dolly_hhrlhf/test'. The data should be formatted with each row containing a
            'prompt' and 'response' field for INSTRUCTION_FINETUNE, or in raw data format for CONTINUED_PRETRAIN.
        save_folder: The remote location to save the finetuned checkpoints. For example,
            if your ``save_folder`` is ``s3://my-bucket/my-checkpoints``, the finetuned Composer checkpoints
            will be saved to ``s3://my-bucket/my-checkpoints/<run-name>/checkpoints``, and Hugging Face formatted
            checkpoints will be saved to ``s3://my-bucket/my-checkpoints/<run-name>/hf_checkpoints``. The supported
            cloud provider prefixes are ``s3://``, ``gs://``, and ``oci://``.
        eval_data_path: The remote location of your evaluation data (e.g. ``s3://my-bucket/my-data.jsonl``). For
            INSTRUCTION_FINETUNE, the name of a Hugging Face dataset with the test split
            (e.g. ``mosaicml/dolly_hhrlhf/test``) can also be given. The evaluation data should be formatted with each
            row containing a ``prompt`` and ``response`` field, for INSTRUCTION_FINETUNE and raw data for
            CONTINUED_PRETRAIN. Default is ``None``.
        custom_weights_path: The remote location of a custom model checkpoint to use for finetuning. If provided,
            these weights will be used instead of the original pretrained weights of the model. This must be a Composer
            checkpoint. Default is ``None``.
        training_duration: The total duration of your finetuning run. This can be specified in batches
            (e.g. ``100ba``), epochs (e.g. ``10ep``), or tokens (e.g. ``1_000_000tok``). Default is ``1ep``.
        learning_rate: The peak learning rate to use for finetuning. Default is ``5e-7``. The optimizer used
            is DecoupledLionW with betas of 0.99 and 0.95 and no weight decay, and the learning rate scheduler used is
            LinearWithWarmupSchedule with a warmup of 2% of the total training duration and a final learning rate 
            multiplier of 0.
        context_length: The maximum sequence length to use. This will be used to truncate any data that is too long. 
            The default is the default for the provided Hugging Face model. We do not support extending the context
            length beyond each model's default. The default context length of each supported model is as follows:
            ``mosaicml/mpt-7b-8k``: 8192, ``mosaicml/mpt-30b``: 8192, ``mosaicml/mpt-7b``: 2048 and for any of the
            meta-llama models: 4096.
        experiment_trackers: A list of experiment tracker configurations. For example, to add Weights and Biases
            tracking, you can pass in ``{'integration_type': 'wandb', 'project': 'my-project',
            'entity': 'my-entity'}``.
        timeout: Time, in seconds, in which the call should complete. If the run creation
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to `create_run` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :type Run: output, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Returns:
        A Run object containing the run information.
    """
    config = FinetuneConfig.from_dict({
        'model': model,
        'task_type': task_type,
        'train_data_path': train_data_path,
        'save_folder': save_folder,
        'eval_data_path': eval_data_path,
        'training_duration': training_duration,
        'experiment_trackers': experiment_trackers,
        'learning_rate': learning_rate,
        'context_length': context_length,
        'custom_weights_path': custom_weights_path,
    })
    finetune_config = config.to_create_finetune_api_input()
    variables = {
        VARIABLE_DATA_NAME: finetune_config,
    }
    response = run_singular_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=Run,
        variables=variables,
    )
    return get_return_response(response, future=future, timeout=timeout)
