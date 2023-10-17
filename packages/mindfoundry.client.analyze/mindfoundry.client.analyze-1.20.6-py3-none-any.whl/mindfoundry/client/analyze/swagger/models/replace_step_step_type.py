from enum import Enum


class ReplaceStepStepType(str, Enum):
    REPLACE = "replace"

    def __str__(self) -> str:
        return str(self.value)