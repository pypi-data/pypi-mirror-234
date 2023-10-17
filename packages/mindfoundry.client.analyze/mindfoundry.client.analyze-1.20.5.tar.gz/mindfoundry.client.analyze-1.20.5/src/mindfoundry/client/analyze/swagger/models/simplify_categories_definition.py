from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.simplify_categories_rule import SimplifyCategoriesRule

T = TypeVar("T", bound="SimplifyCategoriesDefinition")

@attr.s(auto_attribs=True)
class SimplifyCategoriesDefinition:
    """
    Attributes:
        value (str):
        rules (List[SimplifyCategoriesRule]):
    """

    value: str
    rules: List[SimplifyCategoriesRule]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        rules = []
        for rules_item_data in self.rules:
            rules_item = rules_item_data.to_dict()

            rules.append(rules_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "value": value,
            "rules": rules,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value")

        rules = []
        _rules = d.pop("rules")
        for rules_item_data in (_rules):
            rules_item = SimplifyCategoriesRule.from_dict(rules_item_data)



            rules.append(rules_item)


        simplify_categories_definition = cls(
            value=value,
            rules=rules,
        )

        simplify_categories_definition.additional_properties = d
        return simplify_categories_definition

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
