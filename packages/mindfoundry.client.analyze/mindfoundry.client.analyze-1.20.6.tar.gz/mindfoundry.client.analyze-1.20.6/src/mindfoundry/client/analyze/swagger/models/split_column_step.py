from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.split_column_step_step_type import SplitColumnStepStepType

T = TypeVar("T", bound="SplitColumnStep")

@attr.s(auto_attribs=True)
class SplitColumnStep:
    """
    Attributes:
        column (str):
        split_character (str):
        step_type (SplitColumnStepStepType):
    """

    column: str
    split_character: str
    step_type: SplitColumnStepStepType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        column = self.column
        split_character = self.split_character
        step_type = self.step_type.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "column": column,
            "splitCharacter": split_character,
            "stepType": step_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        column = d.pop("column")

        split_character = d.pop("splitCharacter")

        step_type = SplitColumnStepStepType(d.pop("stepType"))




        split_column_step = cls(
            column=column,
            split_character=split_character,
            step_type=step_type,
        )

        split_column_step.additional_properties = d
        return split_column_step

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
