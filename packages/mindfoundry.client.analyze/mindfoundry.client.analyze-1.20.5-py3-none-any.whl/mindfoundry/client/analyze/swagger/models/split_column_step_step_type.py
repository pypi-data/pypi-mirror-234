from enum import Enum


class SplitColumnStepStepType(str, Enum):
    SPLIT = "split"

    def __str__(self) -> str:
        return str(self.value)