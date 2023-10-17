from enum import Enum


class ModelHealth(str, Enum):
    UNKNOWN = "UNKNOWN"
    GOOD = "GOOD"
    BAD = "BAD"

    def __str__(self) -> str:
        return str(self.value)