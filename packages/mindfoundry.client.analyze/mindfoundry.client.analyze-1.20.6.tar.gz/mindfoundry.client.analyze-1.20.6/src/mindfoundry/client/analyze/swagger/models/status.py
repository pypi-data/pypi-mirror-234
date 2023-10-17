from enum import Enum


class Status(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    MISSING = "MISSING"

    def __str__(self) -> str:
        return str(self.value)