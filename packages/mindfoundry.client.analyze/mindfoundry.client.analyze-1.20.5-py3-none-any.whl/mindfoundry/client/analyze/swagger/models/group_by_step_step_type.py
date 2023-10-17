from enum import Enum


class GroupByStepStepType(str, Enum):
    GROUPBY = "groupby"

    def __str__(self) -> str:
        return str(self.value)