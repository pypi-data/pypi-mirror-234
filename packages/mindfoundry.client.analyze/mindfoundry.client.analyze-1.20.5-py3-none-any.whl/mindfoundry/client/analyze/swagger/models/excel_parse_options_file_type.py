from enum import Enum


class ExcelParseOptionsFileType(str, Enum):
    EXCEL = "excel"

    def __str__(self) -> str:
        return str(self.value)