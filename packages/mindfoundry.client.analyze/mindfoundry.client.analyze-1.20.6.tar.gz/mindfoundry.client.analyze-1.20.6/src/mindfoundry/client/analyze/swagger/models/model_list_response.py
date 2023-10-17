from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.model_response import ModelResponse
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelListResponse")

@attr.s(auto_attribs=True)
class ModelListResponse:
    """
    Attributes:
        models (Union[Unset, List[ModelResponse]]):
    """

    models: Union[Unset, List[ModelResponse]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        models: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.models, Unset):
            models = []
            for models_item_data in self.models:
                models_item = models_item_data.to_dict()

                models.append(models_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if models is not UNSET:
            field_dict["models"] = models

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        models = []
        _models = d.pop("models", UNSET)
        for models_item_data in (_models or []):
            models_item = ModelResponse.from_dict(models_item_data)



            models.append(models_item)


        model_list_response = cls(
            models=models,
        )

        model_list_response.additional_properties = d
        return model_list_response

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
