from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.deployed_pipeline_api_response import DeployedPipelineApiResponse
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeployedPipelineApiListResponse")

@attr.s(auto_attribs=True)
class DeployedPipelineApiListResponse:
    """
    Attributes:
        published_pipelines (Union[Unset, List[DeployedPipelineApiResponse]]):
    """

    published_pipelines: Union[Unset, List[DeployedPipelineApiResponse]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        published_pipelines: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.published_pipelines, Unset):
            published_pipelines = []
            for published_pipelines_item_data in self.published_pipelines:
                published_pipelines_item = published_pipelines_item_data.to_dict()

                published_pipelines.append(published_pipelines_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if published_pipelines is not UNSET:
            field_dict["publishedPipelines"] = published_pipelines

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        published_pipelines = []
        _published_pipelines = d.pop("publishedPipelines", UNSET)
        for published_pipelines_item_data in (_published_pipelines or []):
            published_pipelines_item = DeployedPipelineApiResponse.from_dict(published_pipelines_item_data)



            published_pipelines.append(published_pipelines_item)


        deployed_pipeline_api_list_response = cls(
            published_pipelines=published_pipelines,
        )

        deployed_pipeline_api_list_response.additional_properties = d
        return deployed_pipeline_api_list_response

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
