from enum import Enum


class DataPartitionMethod(str, Enum):
    RANDOM = "RANDOM"
    ORDERED = "ORDERED"
    MANUAL = "MANUAL"
    NO_MIXING = "NO_MIXING"

    def __str__(self) -> str:
        return str(self.value)