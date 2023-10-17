from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateDeployedModelApiRequest")

@attr.s(auto_attribs=True)
class UpdateDeployedModelApiRequest:
    """
    Attributes:
        new_model_id (int):
        notes (Union[Unset, None, str]):
    """

    new_model_id: int
    notes: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        new_model_id = self.new_model_id
        notes = self.notes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "newModelId": new_model_id,
        })
        if notes is not UNSET:
            field_dict["notes"] = notes

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        new_model_id = d.pop("newModelId")

        notes = d.pop("notes", UNSET)

        update_deployed_model_api_request = cls(
            new_model_id=new_model_id,
            notes=notes,
        )

        update_deployed_model_api_request.additional_properties = d
        return update_deployed_model_api_request

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
