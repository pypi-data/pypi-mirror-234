from enum import Enum


class FilterRowsRuleRule(str, Enum):
    LESS_THAN = "less_than"
    GREATER_THAN = "greater_than"
    BETWEEN = "between"
    NOT_BETWEEN = "not_between"
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"

    def __str__(self) -> str:
        return str(self.value)