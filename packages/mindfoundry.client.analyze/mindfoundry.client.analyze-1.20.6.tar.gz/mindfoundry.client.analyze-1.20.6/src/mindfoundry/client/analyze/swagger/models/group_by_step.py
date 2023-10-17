from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.group_by_aggregation import GroupByAggregation
from ..models.group_by_step_step_type import GroupByStepStepType

T = TypeVar("T", bound="GroupByStep")

@attr.s(auto_attribs=True)
class GroupByStep:
    """
    Attributes:
        key_columns (List[str]):
        aggregations (List[GroupByAggregation]):
        step_type (GroupByStepStepType):
    """

    key_columns: List[str]
    aggregations: List[GroupByAggregation]
    step_type: GroupByStepStepType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        key_columns = self.key_columns




        aggregations = []
        for aggregations_item_data in self.aggregations:
            aggregations_item = aggregations_item_data.to_dict()

            aggregations.append(aggregations_item)




        step_type = self.step_type.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "keyColumns": key_columns,
            "aggregations": aggregations,
            "stepType": step_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key_columns = cast(List[str], d.pop("keyColumns"))


        aggregations = []
        _aggregations = d.pop("aggregations")
        for aggregations_item_data in (_aggregations):
            aggregations_item = GroupByAggregation.from_dict(aggregations_item_data)



            aggregations.append(aggregations_item)


        step_type = GroupByStepStepType(d.pop("stepType"))




        group_by_step = cls(
            key_columns=key_columns,
            aggregations=aggregations,
            step_type=step_type,
        )

        group_by_step.additional_properties = d
        return group_by_step

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
