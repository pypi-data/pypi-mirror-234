from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="DecisioningThreshold")

@attr.s(auto_attribs=True)
class DecisioningThreshold:
    """
    Attributes:
        upper (float):
        lower (float):
    """

    upper: float
    lower: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        upper = self.upper
        lower = self.lower

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "upper": upper,
            "lower": lower,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        upper = d.pop("upper")

        lower = d.pop("lower")

        decisioning_threshold = cls(
            upper=upper,
            lower=lower,
        )

        decisioning_threshold.additional_properties = d
        return decisioning_threshold

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
