from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.data_set_response import DataSetResponse

T = TypeVar("T", bound="DataSetsResponse")

@attr.s(auto_attribs=True)
class DataSetsResponse:
    """
    Attributes:
        data_sets (List[DataSetResponse]):
    """

    data_sets: List[DataSetResponse]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        data_sets = []
        for data_sets_item_data in self.data_sets:
            data_sets_item = data_sets_item_data.to_dict()

            data_sets.append(data_sets_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "dataSets": data_sets,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data_sets = []
        _data_sets = d.pop("dataSets")
        for data_sets_item_data in (_data_sets):
            data_sets_item = DataSetResponse.from_dict(data_sets_item_data)



            data_sets.append(data_sets_item)


        data_sets_response = cls(
            data_sets=data_sets,
        )

        data_sets_response.additional_properties = d
        return data_sets_response

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
