from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="DecisioningReward")

@attr.s(auto_attribs=True)
class DecisioningReward:
    """
    Attributes:
        class_name (str):
        reward (float):
    """

    class_name: str
    reward: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        class_name = self.class_name
        reward = self.reward

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "className": class_name,
            "reward": reward,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        class_name = d.pop("className")

        reward = d.pop("reward")

        decisioning_reward = cls(
            class_name=class_name,
            reward=reward,
        )

        decisioning_reward.additional_properties = d
        return decisioning_reward

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
