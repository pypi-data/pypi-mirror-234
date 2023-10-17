from enum import Enum


class CreateHttpDataSetRequestDataOrigin(str, Enum):
    HTTP = "http"

    def __str__(self) -> str:
        return str(self.value)