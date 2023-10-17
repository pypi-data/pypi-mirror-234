from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.decisioning_decision import DecisioningDecision

T = TypeVar("T", bound="ConfigureDecisioningRequest")

@attr.s(auto_attribs=True)
class ConfigureDecisioningRequest:
    """
    Attributes:
        target_class (str):
        decisions (List[DecisioningDecision]):
    """

    target_class: str
    decisions: List[DecisioningDecision]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        target_class = self.target_class
        decisions = []
        for decisions_item_data in self.decisions:
            decisions_item = decisions_item_data.to_dict()

            decisions.append(decisions_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "targetClass": target_class,
            "decisions": decisions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        target_class = d.pop("targetClass")

        decisions = []
        _decisions = d.pop("decisions")
        for decisions_item_data in (_decisions):
            decisions_item = DecisioningDecision.from_dict(decisions_item_data)



            decisions.append(decisions_item)


        configure_decisioning_request = cls(
            target_class=target_class,
            decisions=decisions,
        )

        configure_decisioning_request.additional_properties = d
        return configure_decisioning_request

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
