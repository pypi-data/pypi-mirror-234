from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.create_http_data_set_request_data_origin import (
    CreateHttpDataSetRequestDataOrigin,
)
from ..models.csv_parse_options import CsvParseOptions
from ..models.excel_parse_options import ExcelParseOptions
from ..models.json_parse_options import JsonParseOptions
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateHttpDataSetRequest")

@attr.s(auto_attribs=True)
class CreateHttpDataSetRequest:
    """
    Attributes:
        name (str):
        description (str):
        url (str):
        data_origin (CreateHttpDataSetRequestDataOrigin):
        parse_options (Union[CsvParseOptions, ExcelParseOptions, JsonParseOptions, Unset]):  Example: {'fileType':
            'csv', 'columnNamesInHeader': True, 'charset': 'UTF-8'}.
    """

    name: str
    description: str
    url: str
    data_origin: CreateHttpDataSetRequestDataOrigin
    parse_options: Union[CsvParseOptions, ExcelParseOptions, JsonParseOptions, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        url = self.url
        data_origin = self.data_origin.value

        parse_options: Union[Dict[str, Any], Unset]
        if isinstance(self.parse_options, Unset):
            parse_options = UNSET

        elif isinstance(self.parse_options, CsvParseOptions):
            parse_options = self.parse_options.to_dict()

        elif isinstance(self.parse_options, ExcelParseOptions):
            parse_options = self.parse_options.to_dict()

        else:
            parse_options = self.parse_options.to_dict()




        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "description": description,
            "url": url,
            "dataOrigin": data_origin,
        })
        if parse_options is not UNSET:
            field_dict["parseOptions"] = parse_options

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        url = d.pop("url")

        data_origin = CreateHttpDataSetRequestDataOrigin(d.pop("dataOrigin"))




        def _parse_parse_options(data: object) -> Union[CsvParseOptions, ExcelParseOptions, JsonParseOptions, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_parse_options_type_0 = CsvParseOptions.from_dict(data)



                return componentsschemas_parse_options_type_0
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_parse_options_type_1 = ExcelParseOptions.from_dict(data)



                return componentsschemas_parse_options_type_1
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_parse_options_type_2 = JsonParseOptions.from_dict(data)



            return componentsschemas_parse_options_type_2

        parse_options = _parse_parse_options(d.pop("parseOptions", UNSET))


        create_http_data_set_request = cls(
            name=name,
            description=description,
            url=url,
            data_origin=data_origin,
            parse_options=parse_options,
        )

        create_http_data_set_request.additional_properties = d
        return create_http_data_set_request

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
