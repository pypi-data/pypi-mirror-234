from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.filter_rows_rule import FilterRowsRule
from ..models.filter_rows_step_step_type import FilterRowsStepStepType

T = TypeVar("T", bound="FilterRowsStep")

@attr.s(auto_attribs=True)
class FilterRowsStep:
    """
    Attributes:
        rules (List[FilterRowsRule]):
        step_type (FilterRowsStepStepType):
    """

    rules: List[FilterRowsRule]
    step_type: FilterRowsStepStepType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        rules = []
        for rules_item_data in self.rules:
            rules_item = rules_item_data.to_dict()

            rules.append(rules_item)




        step_type = self.step_type.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "rules": rules,
            "stepType": step_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        rules = []
        _rules = d.pop("rules")
        for rules_item_data in (_rules):
            rules_item = FilterRowsRule.from_dict(rules_item_data)



            rules.append(rules_item)


        step_type = FilterRowsStepStepType(d.pop("stepType"))




        filter_rows_step = cls(
            rules=rules,
            step_type=step_type,
        )

        filter_rows_step.additional_properties = d
        return filter_rows_step

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
