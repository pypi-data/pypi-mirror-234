from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.json_parse_options_file_type import JsonParseOptionsFileType

T = TypeVar("T", bound="JsonParseOptions")

@attr.s(auto_attribs=True)
class JsonParseOptions:
    """
    Attributes:
        file_type (JsonParseOptionsFileType):
    """

    file_type: JsonParseOptionsFileType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        file_type = self.file_type.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "fileType": file_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_type = JsonParseOptionsFileType(d.pop("fileType"))




        json_parse_options = cls(
            file_type=file_type,
        )

        json_parse_options.additional_properties = d
        return json_parse_options

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
