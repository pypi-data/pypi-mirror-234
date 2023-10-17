from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..models.decisioning_reward import DecisioningReward
from ..models.decisioning_threshold import DecisioningThreshold
from ..types import UNSET, Unset

T = TypeVar("T", bound="DecisioningDecision")

@attr.s(auto_attribs=True)
class DecisioningDecision:
    """
    Attributes:
        label (str):
        rewards (List[DecisioningReward]):
        chosen_threshold (Optional[DecisioningThreshold]):
        optimal_threshold (Union[Unset, None, DecisioningThreshold]):
    """

    label: str
    rewards: List[DecisioningReward]
    chosen_threshold: Optional[DecisioningThreshold]
    optimal_threshold: Union[Unset, None, DecisioningThreshold] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        rewards = []
        for rewards_item_data in self.rewards:
            rewards_item = rewards_item_data.to_dict()

            rewards.append(rewards_item)




        chosen_threshold = self.chosen_threshold.to_dict() if self.chosen_threshold else None

        optimal_threshold: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.optimal_threshold, Unset):
            optimal_threshold = self.optimal_threshold.to_dict() if self.optimal_threshold else None


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "label": label,
            "rewards": rewards,
            "chosenThreshold": chosen_threshold,
        })
        if optimal_threshold is not UNSET:
            field_dict["optimalThreshold"] = optimal_threshold

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label")

        rewards = []
        _rewards = d.pop("rewards")
        for rewards_item_data in (_rewards):
            rewards_item = DecisioningReward.from_dict(rewards_item_data)



            rewards.append(rewards_item)


        _chosen_threshold = d.pop("chosenThreshold")
        chosen_threshold: Optional[DecisioningThreshold]
        if _chosen_threshold is None:
            chosen_threshold = None
        else:
            chosen_threshold = DecisioningThreshold.from_dict(_chosen_threshold)




        _optimal_threshold = d.pop("optimalThreshold", UNSET)
        optimal_threshold: Union[Unset, None, DecisioningThreshold]
        if _optimal_threshold is None:
            optimal_threshold = None
        elif isinstance(_optimal_threshold,  Unset):
            optimal_threshold = UNSET
        else:
            optimal_threshold = DecisioningThreshold.from_dict(_optimal_threshold)




        decisioning_decision = cls(
            label=label,
            rewards=rewards,
            chosen_threshold=chosen_threshold,
            optimal_threshold=optimal_threshold,
        )

        decisioning_decision.additional_properties = d
        return decisioning_decision

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
