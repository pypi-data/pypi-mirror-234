from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateTestRequest")

@attr.s(auto_attribs=True)
class CreateTestRequest:
    """
    Attributes:
        model_id (int):
        data_set_id (int):
        name (Union[Unset, str]):
        description (Union[Unset, None, str]):
    """

    model_id: int
    data_set_id: int
    name: Union[Unset, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        model_id = self.model_id
        data_set_id = self.data_set_id
        name = self.name
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "modelId": model_id,
            "dataSetId": data_set_id,
        })
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        model_id = d.pop("modelId")

        data_set_id = d.pop("dataSetId")

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        create_test_request = cls(
            model_id=model_id,
            data_set_id=data_set_id,
            name=name,
            description=description,
        )

        create_test_request.additional_properties = d
        return create_test_request

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
