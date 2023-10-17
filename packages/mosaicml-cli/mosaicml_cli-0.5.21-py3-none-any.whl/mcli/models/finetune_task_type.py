""" Defines a Finetune Task Type """
from __future__ import annotations

from enum import Enum
from typing import Optional


class FinetuneTaskType(Enum):
    """ The Type of Finetune Task to run """
    INSTRUCTION_FINETUNE = 'INSTRUCTION_FINETUNE'
    CONTINUED_PRETRAIN = 'CONTINUED_PRETRAIN'

    @classmethod
    def validate_task_type(cls, task_type: Optional[str]) -> bool:
        """ Convert a string to a valid FinetuneTaskType Enum """
        if task_type is None:
            return True
        for e in FinetuneTaskType:
            if e.value == task_type:
                return True

        return False
