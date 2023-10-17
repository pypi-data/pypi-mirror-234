from enum import Enum


class CreateCloudDataSetRequestDataOrigin(str, Enum):
    CLOUD = "cloud"

    def __str__(self) -> str:
        return str(self.value)