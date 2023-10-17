"""Utilities for run epilogs"""
from __future__ import annotations

from logging import Logger
from typing import Optional

from mcli.utils.utils_logging import FAIL, INFO, OK, get_indented_block


class CommonLog():
    """Log some common epilog log outputs
    """

    def __init__(self, logger: Logger):
        self.logger = logger

    def log_timeout(self):
        self.logger.warning(('Run is taking awhile to start, returning you to the command line.\n'
                             'Common causes are the run is queued because the resources are not available '
                             'yet, or the docker image is taking awhile to download.\n\n'
                             'To continue to view job status, use `mcli get runs` and `mcli logs`.'))

    def log_pod_failed_pull(self, run_name: str, image: Optional[str] = None):
        self.logger.error(f'{FAIL} Run {run_name} failed to start and will be deleted because it could '
                          'still be consuming resources.')

        msg = f'Could not find Docker image "{image}"' if image else 'Could not find Docker image'
        error_message = f"""
                    {msg}. If this is a private image, check
                    `mcli get secret` to ensure that you have a Docker secret created. If not, create one
                    using `mcli create secret docker`. Otherwise, double-check your image name.
                """

        self.logger.error(get_indented_block(error_message))

    def log_pod_failed(self, run_name: str):
        self.logger.error(f'{FAIL} Run {run_name} failed. You can check its logs using '
                          f'`mcli logs {run_name}`')

    def log_unknown_did_not_start(self):
        self.logger.warning(f'{INFO} Run did not start for an unknown reason. You can monitor it with '
                            '`mcli get runs` to see if it starts.')

    def log_connect_run_terminating(self, status_display: str):
        self.logger.warning(f'{FAIL} Cannot connect to run, run is already in a {status_display} status.')

    def log_run_interactive_starting(self, run_name: str):
        self.logger.info(f'{OK} Run [cyan]{run_name}[/] has started. Preparing your interactive session...')
