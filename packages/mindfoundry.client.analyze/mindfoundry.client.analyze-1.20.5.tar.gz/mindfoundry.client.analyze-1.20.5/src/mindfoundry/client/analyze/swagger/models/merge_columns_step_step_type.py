from enum import Enum


class MergeColumnsStepStepType(str, Enum):
    MERGE = "merge"

    def __str__(self) -> str:
        return str(self.value)