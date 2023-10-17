from enum import Enum


class RenameStepStepType(str, Enum):
    RENAME = "rename"

    def __str__(self) -> str:
        return str(self.value)