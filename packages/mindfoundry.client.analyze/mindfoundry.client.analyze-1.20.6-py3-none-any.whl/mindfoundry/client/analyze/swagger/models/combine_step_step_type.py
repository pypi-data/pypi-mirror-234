from enum import Enum


class CombineStepStepType(str, Enum):
    JOIN = "join"

    def __str__(self) -> str:
        return str(self.value)