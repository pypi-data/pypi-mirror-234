from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.fill_missing_value_step_step_type import FillMissingValueStepStepType

T = TypeVar("T", bound="FillMissingValueStep")

@attr.s(auto_attribs=True)
class FillMissingValueStep:
    """
    Attributes:
        columns (List[str]):
        default_value (str):
        step_type (FillMissingValueStepStepType):
    """

    columns: List[str]
    default_value: str
    step_type: FillMissingValueStepStepType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        columns = self.columns




        default_value = self.default_value
        step_type = self.step_type.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "columns": columns,
            "defaultValue": default_value,
            "stepType": step_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        columns = cast(List[str], d.pop("columns"))


        default_value = d.pop("defaultValue")

        step_type = FillMissingValueStepStepType(d.pop("stepType"))




        fill_missing_value_step = cls(
            columns=columns,
            default_value=default_value,
            step_type=step_type,
        )

        fill_missing_value_step.additional_properties = d
        return fill_missing_value_step

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
