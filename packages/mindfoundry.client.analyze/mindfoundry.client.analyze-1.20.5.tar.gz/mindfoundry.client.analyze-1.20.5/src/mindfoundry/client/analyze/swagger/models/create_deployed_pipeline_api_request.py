from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateDeployedPipelineApiRequest")

@attr.s(auto_attribs=True)
class CreateDeployedPipelineApiRequest:
    """
    Attributes:
        pipeline_id (int):
        name (str):
        description (Union[Unset, None, str]):
    """

    pipeline_id: int
    name: str
    description: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        pipeline_id = self.pipeline_id
        name = self.name
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "pipelineId": pipeline_id,
            "name": name,
        })
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pipeline_id = d.pop("pipelineId")

        name = d.pop("name")

        description = d.pop("description", UNSET)

        create_deployed_pipeline_api_request = cls(
            pipeline_id=pipeline_id,
            name=name,
            description=description,
        )

        create_deployed_pipeline_api_request.additional_properties = d
        return create_deployed_pipeline_api_request

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
