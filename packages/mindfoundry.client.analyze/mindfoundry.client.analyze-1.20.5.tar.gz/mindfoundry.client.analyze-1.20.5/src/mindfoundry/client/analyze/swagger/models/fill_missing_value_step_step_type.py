from enum import Enum


class FillMissingValueStepStepType(str, Enum):
    IMPUTE = "impute"

    def __str__(self) -> str:
        return str(self.value)