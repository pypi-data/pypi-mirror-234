from enum import Enum


class TransformTextStepStepType(str, Enum):
    REGEX = "regex"

    def __str__(self) -> str:
        return str(self.value)