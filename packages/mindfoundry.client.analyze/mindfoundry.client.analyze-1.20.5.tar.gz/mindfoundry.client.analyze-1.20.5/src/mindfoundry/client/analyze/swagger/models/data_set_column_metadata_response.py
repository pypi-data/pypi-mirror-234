from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.api_column_level import ApiColumnLevel
from ..models.api_column_type import ApiColumnType

T = TypeVar("T", bound="DataSetColumnMetadataResponse")

@attr.s(auto_attribs=True)
class DataSetColumnMetadataResponse:
    """
    Attributes:
        name (str):
        type (ApiColumnType):
        level (ApiColumnLevel):
    """

    name: str
    type: ApiColumnType
    level: ApiColumnLevel
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type = self.type.value

        level = self.level.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "type": type,
            "level": level,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        type = ApiColumnType(d.pop("type"))




        level = ApiColumnLevel(d.pop("level"))




        data_set_column_metadata_response = cls(
            name=name,
            type=type,
            level=level,
        )

        data_set_column_metadata_response.additional_properties = d
        return data_set_column_metadata_response

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
