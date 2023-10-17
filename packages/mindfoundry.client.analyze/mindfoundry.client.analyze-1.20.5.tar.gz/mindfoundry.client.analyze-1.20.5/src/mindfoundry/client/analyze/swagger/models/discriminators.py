from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.discriminators_column_values_item import DiscriminatorsColumnValuesItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="Discriminators")

@attr.s(auto_attribs=True)
class Discriminators:
    """
    Attributes:
        empty (bool):
        column_values (Union[Unset, List[DiscriminatorsColumnValuesItem]]):
    """

    empty: bool
    column_values: Union[Unset, List[DiscriminatorsColumnValuesItem]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        empty = self.empty
        column_values: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.column_values, Unset):
            column_values = []
            for column_values_item_data in self.column_values:
                column_values_item = column_values_item_data.to_dict()

                column_values.append(column_values_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "empty": empty,
        })
        if column_values is not UNSET:
            field_dict["columnValues"] = column_values

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        empty = d.pop("empty")

        column_values = []
        _column_values = d.pop("columnValues", UNSET)
        for column_values_item_data in (_column_values or []):
            column_values_item = DiscriminatorsColumnValuesItem.from_dict(column_values_item_data)



            column_values.append(column_values_item)


        discriminators = cls(
            empty=empty,
            column_values=column_values,
        )

        discriminators.additional_properties = d
        return discriminators

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
