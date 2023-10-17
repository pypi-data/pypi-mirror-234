from enum import Enum


class ModelStatus(str, Enum):
    CONFIGURING = "CONFIGURING"
    BUILDING = "BUILDING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"

    def __str__(self) -> str:
        return str(self.value)