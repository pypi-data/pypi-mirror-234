from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.score_type import ScoreType

T = TypeVar("T", bound="ModelScore")

@attr.s(auto_attribs=True)
class ModelScore:
    """
    Attributes:
        value (float):
        type (ScoreType):
    """

    value: float
    type: ScoreType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        type = self.type.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "value": value,
            "type": type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value")

        type = ScoreType(d.pop("type"))




        model_score = cls(
            value=value,
            type=type,
        )

        model_score.additional_properties = d
        return model_score

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
