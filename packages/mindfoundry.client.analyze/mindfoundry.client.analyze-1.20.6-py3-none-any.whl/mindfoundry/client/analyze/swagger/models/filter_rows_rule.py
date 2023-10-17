from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.filter_rows_rule_rule import FilterRowsRuleRule
from ..types import UNSET, Unset

T = TypeVar("T", bound="FilterRowsRule")

@attr.s(auto_attribs=True)
class FilterRowsRule:
    """
    Attributes:
        rule (FilterRowsRuleRule):
        value1 (Union[Unset, str]):
        inclusive (Union[Unset, bool]):
        inclusive_between (Union[Unset, bool]):
    """

    rule: FilterRowsRuleRule
    value1: Union[Unset, str] = UNSET
    inclusive: Union[Unset, bool] = UNSET
    inclusive_between: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        rule = self.rule.value

        value1 = self.value1
        inclusive = self.inclusive
        inclusive_between = self.inclusive_between

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "rule": rule,
        })
        if value1 is not UNSET:
            field_dict["value1"] = value1
        if inclusive is not UNSET:
            field_dict["inclusive"] = inclusive
        if inclusive_between is not UNSET:
            field_dict["inclusiveBetween"] = inclusive_between

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        rule = FilterRowsRuleRule(d.pop("rule"))




        value1 = d.pop("value1", UNSET)

        inclusive = d.pop("inclusive", UNSET)

        inclusive_between = d.pop("inclusiveBetween", UNSET)

        filter_rows_rule = cls(
            rule=rule,
            value1=value1,
            inclusive=inclusive,
            inclusive_between=inclusive_between,
        )

        filter_rows_rule.additional_properties = d
        return filter_rows_rule

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
