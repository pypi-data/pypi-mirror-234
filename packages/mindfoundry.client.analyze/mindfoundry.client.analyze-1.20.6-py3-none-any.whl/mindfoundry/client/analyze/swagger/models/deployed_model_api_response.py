from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.api_history_response import ApiHistoryResponse
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeployedModelApiResponse")

@attr.s(auto_attribs=True)
class DeployedModelApiResponse:
    """
    Attributes:
        id (int):
        project_id (int):
        name (str):
        api_endpoint (str):
        documentation_endpoint (str):
        history (List[ApiHistoryResponse]):
        description (Union[Unset, None, str]):
    """

    id: int
    project_id: int
    name: str
    api_endpoint: str
    documentation_endpoint: str
    history: List[ApiHistoryResponse]
    description: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        project_id = self.project_id
        name = self.name
        api_endpoint = self.api_endpoint
        documentation_endpoint = self.documentation_endpoint
        history = []
        for history_item_data in self.history:
            history_item = history_item_data.to_dict()

            history.append(history_item)




        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "projectId": project_id,
            "name": name,
            "apiEndpoint": api_endpoint,
            "documentationEndpoint": documentation_endpoint,
            "history": history,
        })
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        project_id = d.pop("projectId")

        name = d.pop("name")

        api_endpoint = d.pop("apiEndpoint")

        documentation_endpoint = d.pop("documentationEndpoint")

        history = []
        _history = d.pop("history")
        for history_item_data in (_history):
            history_item = ApiHistoryResponse.from_dict(history_item_data)



            history.append(history_item)


        description = d.pop("description", UNSET)

        deployed_model_api_response = cls(
            id=id,
            project_id=project_id,
            name=name,
            api_endpoint=api_endpoint,
            documentation_endpoint=documentation_endpoint,
            history=history,
            description=description,
        )

        deployed_model_api_response.additional_properties = d
        return deployed_model_api_response

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
