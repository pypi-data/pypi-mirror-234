from enum import Enum


class GroupByAggregationRule(str, Enum):
    SUM = "sum"
    MEAN = "mean"
    STD_DEV = "std_dev"
    MODE = "mode"
    MIN = "min"
    MAX = "max"
    RANGE = "range"
    COUNT_ALL = "count_all"
    COUNT_NON_NULL = "count_non_null"
    COUNT_NON_NULL_DISTINCT = "count_non_null_distinct"

    def __str__(self) -> str:
        return str(self.value)