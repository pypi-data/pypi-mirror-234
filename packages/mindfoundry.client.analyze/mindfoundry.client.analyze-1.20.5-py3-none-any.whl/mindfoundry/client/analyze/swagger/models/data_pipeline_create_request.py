from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="DataPipelineCreateRequest")

@attr.s(auto_attribs=True)
class DataPipelineCreateRequest:
    """
    Attributes:
        data_set_id (int):
        name (str):
    """

    data_set_id: int
    name: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        data_set_id = self.data_set_id
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "dataSetId": data_set_id,
            "name": name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data_set_id = d.pop("dataSetId")

        name = d.pop("name")

        data_pipeline_create_request = cls(
            data_set_id=data_set_id,
            name=name,
        )

        data_pipeline_create_request.additional_properties = d
        return data_pipeline_create_request

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
