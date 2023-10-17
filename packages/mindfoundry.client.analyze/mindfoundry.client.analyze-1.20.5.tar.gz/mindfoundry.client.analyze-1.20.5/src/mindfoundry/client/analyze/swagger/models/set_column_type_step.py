from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.set_column_type_step_step_type import SetColumnTypeStepStepType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SetColumnTypeStep")

@attr.s(auto_attribs=True)
class SetColumnTypeStep:
    """
    Attributes:
        columns (List[str]):
        new_type (str):
        step_type (SetColumnTypeStepStepType):
        epoch (Union[Unset, str]):
        invalid (Union[Unset, str]):
        not_int (Union[Unset, str]):
        default_not_int (Union[Unset, str]):
        datetime_format (Union[Unset, str]):
        default_value (Union[Unset, str]):
    """

    columns: List[str]
    new_type: str
    step_type: SetColumnTypeStepStepType
    epoch: Union[Unset, str] = UNSET
    invalid: Union[Unset, str] = UNSET
    not_int: Union[Unset, str] = UNSET
    default_not_int: Union[Unset, str] = UNSET
    datetime_format: Union[Unset, str] = UNSET
    default_value: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        columns = self.columns




        new_type = self.new_type
        step_type = self.step_type.value

        epoch = self.epoch
        invalid = self.invalid
        not_int = self.not_int
        default_not_int = self.default_not_int
        datetime_format = self.datetime_format
        default_value = self.default_value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "columns": columns,
            "newType": new_type,
            "stepType": step_type,
        })
        if epoch is not UNSET:
            field_dict["epoch"] = epoch
        if invalid is not UNSET:
            field_dict["invalid"] = invalid
        if not_int is not UNSET:
            field_dict["notInt"] = not_int
        if default_not_int is not UNSET:
            field_dict["defaultNotInt"] = default_not_int
        if datetime_format is not UNSET:
            field_dict["datetimeFormat"] = datetime_format
        if default_value is not UNSET:
            field_dict["defaultValue"] = default_value

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        columns = cast(List[str], d.pop("columns"))


        new_type = d.pop("newType")

        step_type = SetColumnTypeStepStepType(d.pop("stepType"))




        epoch = d.pop("epoch", UNSET)

        invalid = d.pop("invalid", UNSET)

        not_int = d.pop("notInt", UNSET)

        default_not_int = d.pop("defaultNotInt", UNSET)

        datetime_format = d.pop("datetimeFormat", UNSET)

        default_value = d.pop("defaultValue", UNSET)

        set_column_type_step = cls(
            columns=columns,
            new_type=new_type,
            step_type=step_type,
            epoch=epoch,
            invalid=invalid,
            not_int=not_int,
            default_not_int=default_not_int,
            datetime_format=datetime_format,
            default_value=default_value,
        )

        set_column_type_step.additional_properties = d
        return set_column_type_step

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
