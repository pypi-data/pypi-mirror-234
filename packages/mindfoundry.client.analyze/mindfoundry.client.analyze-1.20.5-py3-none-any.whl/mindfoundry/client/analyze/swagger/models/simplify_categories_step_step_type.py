from enum import Enum


class SimplifyCategoriesStepStepType(str, Enum):
    SIMPLIFYCATEGORIES = "simplifyCategories"

    def __str__(self) -> str:
        return str(self.value)