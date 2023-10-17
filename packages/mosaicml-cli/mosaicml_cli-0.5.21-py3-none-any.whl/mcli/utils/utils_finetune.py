"""Helper class for finetuning"""
from datetime import datetime
from time import sleep

from mcli.api.inference_deployments import InferenceDeployment, get_inference_deployment
from mcli.api.runs import Run, RunStatus


# Hugging face model names
class Model():

    def __init__(self, model: str) -> None:
        self.model = model.lower()

    def get_short_name(self):
        return self.model.split('/')[-1]

    def __str__(self) -> str:
        return self.model


def check_run_status_and_raise_if_error(run: Run) -> None:
    start_time = datetime.now()
    while not RunStatus.is_terminal(run.status):
        sleep(10)
        run = run.refresh()
        print(f'Run status: {run.status}, elapsed time: {datetime.now() - start_time}')

    if run.status != RunStatus.COMPLETED:
        print(f'Run failed with status: {run.status}')
        raise RuntimeError(f'Run failed with status: {run.status}')
    print(f'Run completed successfully with status: {run.status}, elapsed time: {datetime.now() - start_time}')


def check_deployment_status_and_raise_if_error(deployment: InferenceDeployment) -> None:
    start_time = datetime.now()
    timeout = 60 * 60  # 1 hour startup time
    while deployment.status not in ['READY', 'FAILED', 'STOPPED']:
        elapsed_time = datetime.now() - start_time
        if elapsed_time.total_seconds() > timeout:
            raise RuntimeError(f'Deployment failed to become READY within {timeout} seconds')
        sleep(10)
        deployment = get_inference_deployment(deployment.name)
        print(f'Deployment status: {deployment.status}, elapsed time: {datetime.now() - start_time}')


def get_mpt_parameters_dict(model_name: str, save_folder: str, train_data_path: str, max_duration: str, gpus: int,
                            max_seq_len: int) -> dict:
    return {
        # Configure autoresumability
        'autoresume': True,
        # Checkpoint to local filesystem or remote object store
        'save_interval': '1ep',  # How frequently to save checkpoints
        'save_num_checkpoints_to_keep': 1,  # Important, this cleans up checkpoints saved to DISK
        # 'save_folder': f'./{run_name}/checkpoints',
        'save_folder': save_folder,
        'dist_timeout': 60000,  # Set large dist_timeout to allow for checkpoint uploading on a slow connection

        # Maximum sequence length of the model
        # For MPT, you can change this to a different number if you would like to train on longer sequences
        # Note that you would also need to reprocess your data to contain longer sequences
        'max_seq_len': max_seq_len,

        # Random seed to ensure reproducibility
        'global_seed': 17,
        'eval_interval': 1,  # How frequently to evaluate the model
        # Model
        # This section is used by LLM-foundry to construct the model
        'model': {
            'name':
                'hf_causal_lm',
            'init_device':
                'mixed',  # Initially only create the model on CPU once per node to reduce system memory requirements
            'pretrained_model_name_or_path':
                model_name,
            'pretrained':
                True,
            'config_overrides':  # Override the default model config (comment this out if you change the model from MPT)
                {
                    'attn_config': {
                        'attn_impl': 'triton',  # Use the triton implementation of attention
                        # We are not concatenating samples together, so this is False
                        # If you turn on packing_ratio below, you may want to set this to True
                        # to restrict attention to within each concatenated sequence
                        # Setting this to True does use some additional GPU memory, so for a large model
                        # and/or large max sequence length, you may want to leave it False.
                        # In our runs, we have successfully trained models both with and without this set to True.
                        'attn_uses_sequence_id': False
                    }
                }
        },

        # Tokenizer
        # This section is used by LLM-foundry to construct the tokenizer
        'tokenizer': {
            'name': model_name,
            'kwargs': {
                'model_max_length': max_seq_len
            }
        },

        # Dataloaders
        # Here we are using the finetuning dataloader
        # see LLM-foundry scripts/train/finetune_example for more details on finetuning data
        'train_loader': {
            'name': 'finetuning',
            'dataset': {
                'hf_name': train_data_path,
                'split': 'train',
                'max_seq_len': max_seq_len,
                'allow_pad_trimming': False,
                'decoder_only_format': True,
                'shuffle': True,
                'shuffle_seed': 17,
            },
            'drop_last': True,
            'num_workers': 8,
            'pin_memory': True,
            'prefetch_factor': 2,
            'persistent_workers': True,
            'timeout': 0
        },

        # Learning rate scheduler
        # see LLM-foundry llmfoundry/utils/builders.py::build_scheduler for other built-in options
        'scheduler': {
            'name': 'linear_decay_with_warmup',
            't_warmup': '0.02dur',
            'alpha_f': 0
        },

        # Optimizer
        # see LLM-foundry llmfoundry/utils/builders.py::build_optimizer for other built-in options
        'optimizer': {  # Based on Dolly
            'name': 'decoupled_lionw',
            'lr': 5.0e-6,
            'betas': [0.9, 0.95],
            'weight_decay': 0
        },

        # Algorithms to apply
        # see LLM-foundry llmfoundry/utils/builders.py::build_algorithm for other built-in options
        'algorithms': {
            'gradient_clipping': {
                'clipping_type': 'norm',
                'clipping_threshold': 1.0
            }
        },

        # Run configuration
        'max_duration':
            max_duration,  # Maximum duration of the run. Change to something shorter (e.g. 10ba) for a quick test run
        'global_train_batch_size': gpus * 6,  # Global batch size. This is the batch size across all GPUs
        'seed': 17,
        'device_train_microbatch_size': 'auto',
        'precision': 'amp_bf16',

        # Configuration settings for FSDP
        # https://docs.mosaicml.com/projects/composer/en/latest/notes/distributed_training.html#fullyshardeddataparallel-fsdp
        # for more information about FSDP in Composer
        'fsdp_config': {
            'sharding_strategy': 'FULL_SHARD',
            'mixed_precision': 'PURE',
            'activation_checkpointing': True,
            'activation_checkpointing_reentrant': False,
            'activation_cpu_offload': False,
            'limit_all_gathers': True,
            'verbose': False
        },

        # Logging configuration
        'progress_bar': False,
        'log_to_console': True,
        'console_log_interval': '10ba',
        'python_log_level': 'debug',
    }
