from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.configure_decisioning_request import ConfigureDecisioningRequest
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateDecisioningRequest")

@attr.s(auto_attribs=True)
class CreateDecisioningRequest:
    """
    Attributes:
        name (str):
        data_set_id (int):
        parent_model_id (int):
        description (Union[Unset, str]):
        configuration (Union[Unset, ConfigureDecisioningRequest]):
    """

    name: str
    data_set_id: int
    parent_model_id: int
    description: Union[Unset, str] = UNSET
    configuration: Union[Unset, ConfigureDecisioningRequest] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        data_set_id = self.data_set_id
        parent_model_id = self.parent_model_id
        description = self.description
        configuration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.configuration, Unset):
            configuration = self.configuration.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "dataSetId": data_set_id,
            "parentModelId": parent_model_id,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if configuration is not UNSET:
            field_dict["configuration"] = configuration

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        data_set_id = d.pop("dataSetId")

        parent_model_id = d.pop("parentModelId")

        description = d.pop("description", UNSET)

        _configuration = d.pop("configuration", UNSET)
        configuration: Union[Unset, ConfigureDecisioningRequest]
        if isinstance(_configuration,  Unset):
            configuration = UNSET
        else:
            configuration = ConfigureDecisioningRequest.from_dict(_configuration)




        create_decisioning_request = cls(
            name=name,
            data_set_id=data_set_id,
            parent_model_id=parent_model_id,
            description=description,
            configuration=configuration,
        )

        create_decisioning_request.additional_properties = d
        return create_decisioning_request

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
