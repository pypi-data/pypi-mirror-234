from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.set_column_level_step_step_type import SetColumnLevelStepStepType

T = TypeVar("T", bound="SetColumnLevelStep")

@attr.s(auto_attribs=True)
class SetColumnLevelStep:
    """
    Attributes:
        columns (List[str]):
        new_level (str):
        step_type (SetColumnLevelStepStepType):
    """

    columns: List[str]
    new_level: str
    step_type: SetColumnLevelStepStepType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        columns = self.columns




        new_level = self.new_level
        step_type = self.step_type.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "columns": columns,
            "newLevel": new_level,
            "stepType": step_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        columns = cast(List[str], d.pop("columns"))


        new_level = d.pop("newLevel")

        step_type = SetColumnLevelStepStepType(d.pop("stepType"))




        set_column_level_step = cls(
            columns=columns,
            new_level=new_level,
            step_type=step_type,
        )

        set_column_level_step.additional_properties = d
        return set_column_level_step

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
