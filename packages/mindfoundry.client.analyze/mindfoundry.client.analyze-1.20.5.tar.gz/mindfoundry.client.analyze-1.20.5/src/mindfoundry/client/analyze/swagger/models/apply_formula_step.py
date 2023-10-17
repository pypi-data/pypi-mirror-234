from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.apply_formula_step_step_type import ApplyFormulaStepStepType

T = TypeVar("T", bound="ApplyFormulaStep")

@attr.s(auto_attribs=True)
class ApplyFormulaStep:
    """
    Attributes:
        formula (str):
        result_column_name (str):
        step_type (ApplyFormulaStepStepType):
    """

    formula: str
    result_column_name: str
    step_type: ApplyFormulaStepStepType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        formula = self.formula
        result_column_name = self.result_column_name
        step_type = self.step_type.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "formula": formula,
            "resultColumnName": result_column_name,
            "stepType": step_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        formula = d.pop("formula")

        result_column_name = d.pop("resultColumnName")

        step_type = ApplyFormulaStepStepType(d.pop("stepType"))




        apply_formula_step = cls(
            formula=formula,
            result_column_name=result_column_name,
            step_type=step_type,
        )

        apply_formula_step.additional_properties = d
        return apply_formula_step

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
