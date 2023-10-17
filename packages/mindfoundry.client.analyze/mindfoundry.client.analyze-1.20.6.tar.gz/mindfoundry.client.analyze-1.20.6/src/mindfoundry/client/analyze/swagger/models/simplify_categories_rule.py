from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="SimplifyCategoriesRule")

@attr.s(auto_attribs=True)
class SimplifyCategoriesRule:
    """
    Attributes:
        matcher (str):
        enable_regex (bool):
        enable_case_sensitive (bool):  Default: True.
    """

    matcher: str
    enable_regex: bool = False
    enable_case_sensitive: bool = True
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        matcher = self.matcher
        enable_regex = self.enable_regex
        enable_case_sensitive = self.enable_case_sensitive

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "matcher": matcher,
            "enableRegex": enable_regex,
            "enableCaseSensitive": enable_case_sensitive,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        matcher = d.pop("matcher")

        enable_regex = d.pop("enableRegex")

        enable_case_sensitive = d.pop("enableCaseSensitive")

        simplify_categories_rule = cls(
            matcher=matcher,
            enable_regex=enable_regex,
            enable_case_sensitive=enable_case_sensitive,
        )

        simplify_categories_rule.additional_properties = d
        return simplify_categories_rule

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
