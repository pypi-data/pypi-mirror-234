from enum import Enum


class CsvParseOptionsFileType(str, Enum):
    CSV = "csv"

    def __str__(self) -> str:
        return str(self.value)