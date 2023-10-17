from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.transform_text_step_if_no_match import TransformTextStepIfNoMatch
from ..models.transform_text_step_replace_existing_column import (
    TransformTextStepReplaceExistingColumn,
)
from ..models.transform_text_step_step_type import TransformTextStepStepType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TransformTextStep")

@attr.s(auto_attribs=True)
class TransformTextStep:
    """
    Attributes:
        column (str):
        input_regex (str):
        if_no_match (TransformTextStepIfNoMatch):
        step_type (TransformTextStepStepType):
        ignore_case (Union[Unset, bool]):
        output_regex (Union[Unset, str]):
        new_column_name (Union[Unset, str]):
        replace_existing_column (Union[Unset, TransformTextStepReplaceExistingColumn]):
    """

    column: str
    input_regex: str
    if_no_match: TransformTextStepIfNoMatch
    step_type: TransformTextStepStepType
    ignore_case: Union[Unset, bool] = UNSET
    output_regex: Union[Unset, str] = UNSET
    new_column_name: Union[Unset, str] = UNSET
    replace_existing_column: Union[Unset, TransformTextStepReplaceExistingColumn] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        column = self.column
        input_regex = self.input_regex
        if_no_match = self.if_no_match.value

        step_type = self.step_type.value

        ignore_case = self.ignore_case
        output_regex = self.output_regex
        new_column_name = self.new_column_name
        replace_existing_column: Union[Unset, str] = UNSET
        if not isinstance(self.replace_existing_column, Unset):
            replace_existing_column = self.replace_existing_column.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "column": column,
            "inputRegex": input_regex,
            "ifNoMatch": if_no_match,
            "stepType": step_type,
        })
        if ignore_case is not UNSET:
            field_dict["ignoreCase"] = ignore_case
        if output_regex is not UNSET:
            field_dict["outputRegex"] = output_regex
        if new_column_name is not UNSET:
            field_dict["newColumnName"] = new_column_name
        if replace_existing_column is not UNSET:
            field_dict["replaceExistingColumn"] = replace_existing_column

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        column = d.pop("column")

        input_regex = d.pop("inputRegex")

        if_no_match = TransformTextStepIfNoMatch(d.pop("ifNoMatch"))




        step_type = TransformTextStepStepType(d.pop("stepType"))




        ignore_case = d.pop("ignoreCase", UNSET)

        output_regex = d.pop("outputRegex", UNSET)

        new_column_name = d.pop("newColumnName", UNSET)

        _replace_existing_column = d.pop("replaceExistingColumn", UNSET)
        replace_existing_column: Union[Unset, TransformTextStepReplaceExistingColumn]
        if isinstance(_replace_existing_column,  Unset):
            replace_existing_column = UNSET
        else:
            replace_existing_column = TransformTextStepReplaceExistingColumn(_replace_existing_column)




        transform_text_step = cls(
            column=column,
            input_regex=input_regex,
            if_no_match=if_no_match,
            step_type=step_type,
            ignore_case=ignore_case,
            output_regex=output_regex,
            new_column_name=new_column_name,
            replace_existing_column=replace_existing_column,
        )

        transform_text_step.additional_properties = d
        return transform_text_step

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
