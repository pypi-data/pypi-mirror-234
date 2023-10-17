from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.set_time_index_step_step_type import SetTimeIndexStepStepType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SetTimeIndexStep")

@attr.s(auto_attribs=True)
class SetTimeIndexStep:
    """
    Attributes:
        column (str):
        step_type (SetTimeIndexStepStepType):
        series_columns (Union[Unset, List[str]]):
    """

    column: str
    step_type: SetTimeIndexStepStepType
    series_columns: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        column = self.column
        step_type = self.step_type.value

        series_columns: Union[Unset, List[str]] = UNSET
        if not isinstance(self.series_columns, Unset):
            series_columns = self.series_columns





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "column": column,
            "stepType": step_type,
        })
        if series_columns is not UNSET:
            field_dict["seriesColumns"] = series_columns

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        column = d.pop("column")

        step_type = SetTimeIndexStepStepType(d.pop("stepType"))




        series_columns = cast(List[str], d.pop("seriesColumns", UNSET))


        set_time_index_step = cls(
            column=column,
            step_type=step_type,
            series_columns=series_columns,
        )

        set_time_index_step.additional_properties = d
        return set_time_index_step

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
