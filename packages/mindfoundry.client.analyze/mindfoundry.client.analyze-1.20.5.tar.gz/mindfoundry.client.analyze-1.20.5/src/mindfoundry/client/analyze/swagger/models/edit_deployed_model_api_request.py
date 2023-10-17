from typing import Any, Dict, List, Optional, Type, TypeVar

import attr

T = TypeVar("T", bound="EditDeployedModelApiRequest")

@attr.s(auto_attribs=True)
class EditDeployedModelApiRequest:
    """
    Attributes:
        name (str):
        description (Optional[str]):
    """

    name: str
    description: Optional[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "description": description,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        edit_deployed_model_api_request = cls(
            name=name,
            description=description,
        )

        edit_deployed_model_api_request.additional_properties = d
        return edit_deployed_model_api_request

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
