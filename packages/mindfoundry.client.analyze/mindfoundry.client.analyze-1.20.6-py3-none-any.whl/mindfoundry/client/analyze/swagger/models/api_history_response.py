import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="ApiHistoryResponse")

@attr.s(auto_attribs=True)
class ApiHistoryResponse:
    """
    Attributes:
        version_number (int):
        created_at (datetime.datetime):
        note (Optional[str]):
        created_by (Optional[str]):
        entity_id (Optional[int]):
        entity_name (Optional[str]):
    """

    version_number: int
    created_at: datetime.datetime
    note: Optional[str]
    created_by: Optional[str]
    entity_id: Optional[int]
    entity_name: Optional[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        version_number = self.version_number
        created_at = self.created_at.isoformat()

        note = self.note
        created_by = self.created_by
        entity_id = self.entity_id
        entity_name = self.entity_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "versionNumber": version_number,
            "createdAt": created_at,
            "note": note,
            "createdBy": created_by,
            "entityId": entity_id,
            "entityName": entity_name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        version_number = d.pop("versionNumber")

        created_at = isoparse(d.pop("createdAt"))




        note = d.pop("note")

        created_by = d.pop("createdBy")

        entity_id = d.pop("entityId")

        entity_name = d.pop("entityName")

        api_history_response = cls(
            version_number=version_number,
            created_at=created_at,
            note=note,
            created_by=created_by,
            entity_id=entity_id,
            entity_name=entity_name,
        )

        api_history_response.additional_properties = d
        return api_history_response

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
