from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="DeleteDataPrepStepsRequest")

@attr.s(auto_attribs=True)
class DeleteDataPrepStepsRequest:
    """
    Attributes:
        delete_index (int): Index of the step to delete
        delete_children (bool): If true, also delete all subsequent steps
    """

    delete_index: int
    delete_children: bool
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        delete_index = self.delete_index
        delete_children = self.delete_children

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "deleteIndex": delete_index,
            "deleteChildren": delete_children,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        delete_index = d.pop("deleteIndex")

        delete_children = d.pop("deleteChildren")

        delete_data_prep_steps_request = cls(
            delete_index=delete_index,
            delete_children=delete_children,
        )

        delete_data_prep_steps_request.additional_properties = d
        return delete_data_prep_steps_request

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
