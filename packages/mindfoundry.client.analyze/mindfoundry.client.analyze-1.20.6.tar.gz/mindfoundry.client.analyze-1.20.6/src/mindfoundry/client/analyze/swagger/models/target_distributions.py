from enum import Enum


class TargetDistributions(str, Enum):
    GAUSSIAN = "GAUSSIAN"
    POISSON = "POISSON"
    GAMMA = "GAMMA"

    def __str__(self) -> str:
        return str(self.value)