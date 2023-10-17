from enum import Enum


class NormalizeTextStepRule(str, Enum):
    LOWER = "lower"
    UPPER = "upper"

    def __str__(self) -> str:
        return str(self.value)