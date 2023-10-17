from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.data_pipeline_response import DataPipelineResponse
from ..types import UNSET, Unset

T = TypeVar("T", bound="DataPipelinesResponse")

@attr.s(auto_attribs=True)
class DataPipelinesResponse:
    """
    Attributes:
        pipelines (Union[Unset, List[DataPipelineResponse]]):
    """

    pipelines: Union[Unset, List[DataPipelineResponse]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        pipelines: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.pipelines, Unset):
            pipelines = []
            for pipelines_item_data in self.pipelines:
                pipelines_item = pipelines_item_data.to_dict()

                pipelines.append(pipelines_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if pipelines is not UNSET:
            field_dict["pipelines"] = pipelines

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pipelines = []
        _pipelines = d.pop("pipelines", UNSET)
        for pipelines_item_data in (_pipelines or []):
            pipelines_item = DataPipelineResponse.from_dict(pipelines_item_data)



            pipelines.append(pipelines_item)


        data_pipelines_response = cls(
            pipelines=pipelines,
        )

        data_pipelines_response.additional_properties = d
        return data_pipelines_response

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
