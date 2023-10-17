from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="DeployedApiClientResponse")

@attr.s(auto_attribs=True)
class DeployedApiClientResponse:
    """
    Attributes:
        id (str):
        project_id (str):
        name (str):
        created_at (str):
        created_by (str):
    """

    id: str
    project_id: str
    name: str
    created_at: str
    created_by: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        project_id = self.project_id
        name = self.name
        created_at = self.created_at
        created_by = self.created_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "projectId": project_id,
            "name": name,
            "createdAt": created_at,
            "createdBy": created_by,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        project_id = d.pop("projectId")

        name = d.pop("name")

        created_at = d.pop("createdAt")

        created_by = d.pop("createdBy")

        deployed_api_client_response = cls(
            id=id,
            project_id=project_id,
            name=name,
            created_at=created_at,
            created_by=created_by,
        )

        deployed_api_client_response.additional_properties = d
        return deployed_api_client_response

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
