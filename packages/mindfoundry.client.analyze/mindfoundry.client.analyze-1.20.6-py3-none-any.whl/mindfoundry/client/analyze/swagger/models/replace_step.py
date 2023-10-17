from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.replace_step_step_type import ReplaceStepStepType

T = TypeVar("T", bound="ReplaceStep")

@attr.s(auto_attribs=True)
class ReplaceStep:
    """
    Attributes:
        columns (List[str]):
        old_value (str):
        new_value (str):
        step_type (ReplaceStepStepType):
    """

    columns: List[str]
    old_value: str
    new_value: str
    step_type: ReplaceStepStepType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        columns = self.columns




        old_value = self.old_value
        new_value = self.new_value
        step_type = self.step_type.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "columns": columns,
            "oldValue": old_value,
            "newValue": new_value,
            "stepType": step_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        columns = cast(List[str], d.pop("columns"))


        old_value = d.pop("oldValue")

        new_value = d.pop("newValue")

        step_type = ReplaceStepStepType(d.pop("stepType"))




        replace_step = cls(
            columns=columns,
            old_value=old_value,
            new_value=new_value,
            step_type=step_type,
        )

        replace_step.additional_properties = d
        return replace_step

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
