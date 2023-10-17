from enum import Enum


class FilterRowsStepStepType(str, Enum):
    FILTER = "filter"

    def __str__(self) -> str:
        return str(self.value)