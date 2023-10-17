from enum import Enum


class DropStepStepType(str, Enum):
    DROP = "drop"

    def __str__(self) -> str:
        return str(self.value)