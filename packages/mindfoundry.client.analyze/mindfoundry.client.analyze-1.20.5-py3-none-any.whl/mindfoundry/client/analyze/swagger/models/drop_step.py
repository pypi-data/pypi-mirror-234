from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.drop_step_step_type import DropStepStepType

T = TypeVar("T", bound="DropStep")

@attr.s(auto_attribs=True)
class DropStep:
    """
    Attributes:
        columns (List[str]):
        step_type (DropStepStepType):
    """

    columns: List[str]
    step_type: DropStepStepType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        columns = self.columns




        step_type = self.step_type.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "columns": columns,
            "stepType": step_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        columns = cast(List[str], d.pop("columns"))


        step_type = DropStepStepType(d.pop("stepType"))




        drop_step = cls(
            columns=columns,
            step_type=step_type,
        )

        drop_step.additional_properties = d
        return drop_step

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
