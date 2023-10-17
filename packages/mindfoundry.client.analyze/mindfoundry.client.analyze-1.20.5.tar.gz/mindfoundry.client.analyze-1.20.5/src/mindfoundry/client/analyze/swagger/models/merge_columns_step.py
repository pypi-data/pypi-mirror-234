from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.merge_columns_step_step_type import MergeColumnsStepStepType

T = TypeVar("T", bound="MergeColumnsStep")

@attr.s(auto_attribs=True)
class MergeColumnsStep:
    """
    Attributes:
        columns (List[str]):
        merged_column_name (str):
        step_type (MergeColumnsStepStepType):
    """

    columns: List[str]
    merged_column_name: str
    step_type: MergeColumnsStepStepType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        columns = self.columns




        merged_column_name = self.merged_column_name
        step_type = self.step_type.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "columns": columns,
            "mergedColumnName": merged_column_name,
            "stepType": step_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        columns = cast(List[str], d.pop("columns"))


        merged_column_name = d.pop("mergedColumnName")

        step_type = MergeColumnsStepStepType(d.pop("stepType"))




        merge_columns_step = cls(
            columns=columns,
            merged_column_name=merged_column_name,
            step_type=step_type,
        )

        merge_columns_step.additional_properties = d
        return merge_columns_step

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
