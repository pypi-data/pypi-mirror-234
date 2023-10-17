from enum import Enum


class RegressionScorers(str, Enum):
    RMSE = "RMSE"
    ABSOLUTE_ERROR = "ABSOLUTE_ERROR"
    R2 = "R2"
    LOG_LIKELIHOOD = "LOG_LIKELIHOOD"
    GINI = "GINI"

    def __str__(self) -> str:
        return str(self.value)