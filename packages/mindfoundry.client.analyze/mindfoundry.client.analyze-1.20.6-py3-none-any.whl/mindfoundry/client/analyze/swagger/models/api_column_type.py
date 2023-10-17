from enum import Enum


class ApiColumnType(str, Enum):
    TEXT = "TEXT"
    FLOAT = "FLOAT"
    INT = "INT"
    DATETIME = "DATETIME"
    UNKNOWN = "UNKNOWN"

    def __str__(self) -> str:
        return str(self.value)