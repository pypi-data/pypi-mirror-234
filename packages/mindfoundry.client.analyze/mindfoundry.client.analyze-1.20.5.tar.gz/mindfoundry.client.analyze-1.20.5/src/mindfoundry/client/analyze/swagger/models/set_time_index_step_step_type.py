from enum import Enum


class SetTimeIndexStepStepType(str, Enum):
    TIME = "time"

    def __str__(self) -> str:
        return str(self.value)