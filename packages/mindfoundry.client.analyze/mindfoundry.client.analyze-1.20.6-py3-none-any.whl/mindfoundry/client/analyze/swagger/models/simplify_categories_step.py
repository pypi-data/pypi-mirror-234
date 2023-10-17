from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.simplify_categories_definition import SimplifyCategoriesDefinition
from ..models.simplify_categories_step_step_type import SimplifyCategoriesStepStepType

T = TypeVar("T", bound="SimplifyCategoriesStep")

@attr.s(auto_attribs=True)
class SimplifyCategoriesStep:
    """
    Attributes:
        column (str):
        new_column_name (str):
        category_definitions (List[SimplifyCategoriesDefinition]):
        step_type (SimplifyCategoriesStepStepType):
    """

    column: str
    new_column_name: str
    category_definitions: List[SimplifyCategoriesDefinition]
    step_type: SimplifyCategoriesStepStepType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        column = self.column
        new_column_name = self.new_column_name
        category_definitions = []
        for category_definitions_item_data in self.category_definitions:
            category_definitions_item = category_definitions_item_data.to_dict()

            category_definitions.append(category_definitions_item)




        step_type = self.step_type.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "column": column,
            "newColumnName": new_column_name,
            "categoryDefinitions": category_definitions,
            "stepType": step_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        column = d.pop("column")

        new_column_name = d.pop("newColumnName")

        category_definitions = []
        _category_definitions = d.pop("categoryDefinitions")
        for category_definitions_item_data in (_category_definitions):
            category_definitions_item = SimplifyCategoriesDefinition.from_dict(category_definitions_item_data)



            category_definitions.append(category_definitions_item)


        step_type = SimplifyCategoriesStepStepType(d.pop("stepType"))




        simplify_categories_step = cls(
            column=column,
            new_column_name=new_column_name,
            category_definitions=category_definitions,
            step_type=step_type,
        )

        simplify_categories_step.additional_properties = d
        return simplify_categories_step

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
