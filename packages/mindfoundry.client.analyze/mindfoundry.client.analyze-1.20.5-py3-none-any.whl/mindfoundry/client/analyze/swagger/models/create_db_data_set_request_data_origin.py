from enum import Enum


class CreateDbDataSetRequestDataOrigin(str, Enum):
    DB = "db"

    def __str__(self) -> str:
        return str(self.value)