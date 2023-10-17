from enum import Enum


class SetColumnLevelStepStepType(str, Enum):
    LEVEL = "level"

    def __str__(self) -> str:
        return str(self.value)