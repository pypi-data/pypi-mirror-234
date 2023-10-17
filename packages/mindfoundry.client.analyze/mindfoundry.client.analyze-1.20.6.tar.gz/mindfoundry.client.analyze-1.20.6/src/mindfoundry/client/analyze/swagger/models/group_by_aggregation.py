from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.group_by_aggregation_rule import GroupByAggregationRule

T = TypeVar("T", bound="GroupByAggregation")

@attr.s(auto_attribs=True)
class GroupByAggregation:
    """
    Attributes:
        target_column (str):
        new_column_name (str):
        rule (GroupByAggregationRule):
    """

    target_column: str
    new_column_name: str
    rule: GroupByAggregationRule
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        target_column = self.target_column
        new_column_name = self.new_column_name
        rule = self.rule.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "targetColumn": target_column,
            "newColumnName": new_column_name,
            "rule": rule,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        target_column = d.pop("targetColumn")

        new_column_name = d.pop("newColumnName")

        rule = GroupByAggregationRule(d.pop("rule"))




        group_by_aggregation = cls(
            target_column=target_column,
            new_column_name=new_column_name,
            rule=rule,
        )

        group_by_aggregation.additional_properties = d
        return group_by_aggregation

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
