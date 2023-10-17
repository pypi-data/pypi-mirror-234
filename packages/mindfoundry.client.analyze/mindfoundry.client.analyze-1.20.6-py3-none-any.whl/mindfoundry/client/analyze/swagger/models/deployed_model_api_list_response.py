from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.deployed_model_api_response import DeployedModelApiResponse
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeployedModelApiListResponse")

@attr.s(auto_attribs=True)
class DeployedModelApiListResponse:
    """
    Attributes:
        published_models (Union[Unset, List[DeployedModelApiResponse]]):
    """

    published_models: Union[Unset, List[DeployedModelApiResponse]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        published_models: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.published_models, Unset):
            published_models = []
            for published_models_item_data in self.published_models:
                published_models_item = published_models_item_data.to_dict()

                published_models.append(published_models_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if published_models is not UNSET:
            field_dict["publishedModels"] = published_models

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        published_models = []
        _published_models = d.pop("publishedModels", UNSET)
        for published_models_item_data in (_published_models or []):
            published_models_item = DeployedModelApiResponse.from_dict(published_models_item_data)



            published_models.append(published_models_item)


        deployed_model_api_list_response = cls(
            published_models=published_models,
        )

        deployed_model_api_list_response.additional_properties = d
        return deployed_model_api_list_response

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
