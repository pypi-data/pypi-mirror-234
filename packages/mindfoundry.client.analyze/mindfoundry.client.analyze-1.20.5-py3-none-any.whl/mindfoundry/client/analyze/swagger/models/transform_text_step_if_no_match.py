from enum import Enum


class TransformTextStepIfNoMatch(str, Enum):
    PASS = "pass"
    BLANK = "blank"

    def __str__(self) -> str:
        return str(self.value)