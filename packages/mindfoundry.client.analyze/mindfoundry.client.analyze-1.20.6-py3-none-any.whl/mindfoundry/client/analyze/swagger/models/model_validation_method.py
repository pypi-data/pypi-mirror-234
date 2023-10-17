from enum import Enum


class ModelValidationMethod(str, Enum):
    TEN_FOLD_CROSS = "TEN_FOLD_CROSS"
    FIVE_FOLD_CROSS = "FIVE_FOLD_CROSS"
    TRAIN_TEST = "TRAIN_TEST"

    def __str__(self) -> str:
        return str(self.value)