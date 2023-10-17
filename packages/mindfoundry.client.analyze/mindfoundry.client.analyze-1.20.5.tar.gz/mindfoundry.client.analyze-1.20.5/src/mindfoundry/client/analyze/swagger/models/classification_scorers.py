from enum import Enum


class ClassificationScorers(str, Enum):
    F1_WEIGHTED_AVG = "F1_WEIGHTED_AVG"
    ACCURACY = "ACCURACY"
    ROC_AUC = "ROC_AUC"
    F1_SINGLE_CLASS = "F1_SINGLE_CLASS"
    RECALL_SINGLE_CLASS = "RECALL_SINGLE_CLASS"
    PRECISION_SINGLE_CLASS = "PRECISION_SINGLE_CLASS"

    def __str__(self) -> str:
        return str(self.value)