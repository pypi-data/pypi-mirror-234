from enum import Enum


class NormalizeTextStepStepType(str, Enum):
    NORMALIZETEXT = "normalizeText"

    def __str__(self) -> str:
        return str(self.value)