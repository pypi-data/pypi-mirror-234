from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.combine_step_step_type import CombineStepStepType

T = TypeVar("T", bound="CombineStep")

@attr.s(auto_attribs=True)
class CombineStep:
    """
    Attributes:
        column (str):
        data_set_column (str):
        data_set_id (int):
        step_type (CombineStepStepType):
    """

    column: str
    data_set_column: str
    data_set_id: int
    step_type: CombineStepStepType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        column = self.column
        data_set_column = self.data_set_column
        data_set_id = self.data_set_id
        step_type = self.step_type.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "column": column,
            "dataSetColumn": data_set_column,
            "dataSetId": data_set_id,
            "stepType": step_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        column = d.pop("column")

        data_set_column = d.pop("dataSetColumn")

        data_set_id = d.pop("dataSetId")

        step_type = CombineStepStepType(d.pop("stepType"))




        combine_step = cls(
            column=column,
            data_set_column=data_set_column,
            data_set_id=data_set_id,
            step_type=step_type,
        )

        combine_step.additional_properties = d
        return combine_step

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
