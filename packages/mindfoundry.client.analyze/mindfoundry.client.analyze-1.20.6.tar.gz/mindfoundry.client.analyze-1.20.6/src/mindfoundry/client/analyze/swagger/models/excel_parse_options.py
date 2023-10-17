from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.excel_parse_options_file_type import ExcelParseOptionsFileType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExcelParseOptions")

@attr.s(auto_attribs=True)
class ExcelParseOptions:
    """
    Attributes:
        file_type (ExcelParseOptionsFileType):
        column_names_in_header (Union[Unset, bool]): The first row contains column names
        skip_top (Union[Unset, int]): Ignore the first n rows
        skip_bottom (Union[Unset, int]): Ignore the last n rows
    """

    file_type: ExcelParseOptionsFileType
    column_names_in_header: Union[Unset, bool] = False
    skip_top: Union[Unset, int] = 0
    skip_bottom: Union[Unset, int] = 0
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        file_type = self.file_type.value

        column_names_in_header = self.column_names_in_header
        skip_top = self.skip_top
        skip_bottom = self.skip_bottom

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "fileType": file_type,
        })
        if column_names_in_header is not UNSET:
            field_dict["columnNamesInHeader"] = column_names_in_header
        if skip_top is not UNSET:
            field_dict["skipTop"] = skip_top
        if skip_bottom is not UNSET:
            field_dict["skipBottom"] = skip_bottom

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_type = ExcelParseOptionsFileType(d.pop("fileType"))




        column_names_in_header = d.pop("columnNamesInHeader", UNSET)

        skip_top = d.pop("skipTop", UNSET)

        skip_bottom = d.pop("skipBottom", UNSET)

        excel_parse_options = cls(
            file_type=file_type,
            column_names_in_header=column_names_in_header,
            skip_top=skip_top,
            skip_bottom=skip_bottom,
        )

        excel_parse_options.additional_properties = d
        return excel_parse_options

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
