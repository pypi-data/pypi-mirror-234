from enum import Enum


class ApplyFormulaStepStepType(str, Enum):
    CALCULATE = "calculate"

    def __str__(self) -> str:
        return str(self.value)