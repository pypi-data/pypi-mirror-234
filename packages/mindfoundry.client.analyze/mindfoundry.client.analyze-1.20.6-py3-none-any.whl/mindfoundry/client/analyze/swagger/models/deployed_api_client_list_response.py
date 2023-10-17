from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.deployed_api_client_response import DeployedApiClientResponse
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeployedApiClientListResponse")

@attr.s(auto_attribs=True)
class DeployedApiClientListResponse:
    """
    Attributes:
        api_clients (Union[Unset, List[DeployedApiClientResponse]]):
    """

    api_clients: Union[Unset, List[DeployedApiClientResponse]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        api_clients: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.api_clients, Unset):
            api_clients = []
            for api_clients_item_data in self.api_clients:
                api_clients_item = api_clients_item_data.to_dict()

                api_clients.append(api_clients_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if api_clients is not UNSET:
            field_dict["apiClients"] = api_clients

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        api_clients = []
        _api_clients = d.pop("apiClients", UNSET)
        for api_clients_item_data in (_api_clients or []):
            api_clients_item = DeployedApiClientResponse.from_dict(api_clients_item_data)



            api_clients.append(api_clients_item)


        deployed_api_client_list_response = cls(
            api_clients=api_clients,
        )

        deployed_api_client_list_response.additional_properties = d
        return deployed_api_client_list_response

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
