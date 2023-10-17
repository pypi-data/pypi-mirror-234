from enum import Enum


class TransformTextStepReplaceExistingColumn(str, Enum):
    REPLACE = "replace"
    NEW_TARGET = "new_target"

    def __str__(self) -> str:
        return str(self.value)