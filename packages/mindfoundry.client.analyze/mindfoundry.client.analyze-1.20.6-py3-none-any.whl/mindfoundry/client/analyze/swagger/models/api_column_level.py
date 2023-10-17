from enum import Enum


class ApiColumnLevel(str, Enum):
    COMPLEX = "COMPLEX"
    MEANINGFUL = "MEANINGFUL"
    UNKNOWN = "UNKNOWN"
    DISCRETE_NOMINAL = "DISCRETE_NOMINAL"
    DISCRETE_ORDINAL = "DISCRETE_ORDINAL"
    DISCRETE_INTERVAL = "DISCRETE_INTERVAL"
    CONTINUOUS_INTERVAL = "CONTINUOUS_INTERVAL"

    def __str__(self) -> str:
        return str(self.value)