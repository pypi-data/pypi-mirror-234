from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.create_db_data_set_request_data_origin import (
    CreateDbDataSetRequestDataOrigin,
)
from ..models.create_db_data_set_request_db_type import CreateDbDataSetRequestDbType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateDbDataSetRequest")

@attr.s(auto_attribs=True)
class CreateDbDataSetRequest:
    """
    Attributes:
        name (str):
        db_type (CreateDbDataSetRequestDbType):
        query (str):
        data_origin (CreateDbDataSetRequestDataOrigin):
        description (Union[Unset, str]):
        username (Union[Unset, str]):
        password (Union[Unset, str]):
        host (Union[Unset, str]):
        port (Union[Unset, str]):
        db_name (Union[Unset, str]):
        custom_db_url (Union[Unset, bool]):
        db_url (Union[Unset, str]): required if customDbUrl is true
    """

    name: str
    db_type: CreateDbDataSetRequestDbType
    query: str
    data_origin: CreateDbDataSetRequestDataOrigin
    description: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    host: Union[Unset, str] = UNSET
    port: Union[Unset, str] = UNSET
    db_name: Union[Unset, str] = UNSET
    custom_db_url: Union[Unset, bool] = False
    db_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        db_type = self.db_type.value

        query = self.query
        data_origin = self.data_origin.value

        description = self.description
        username = self.username
        password = self.password
        host = self.host
        port = self.port
        db_name = self.db_name
        custom_db_url = self.custom_db_url
        db_url = self.db_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "dbType": db_type,
            "query": query,
            "dataOrigin": data_origin,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if username is not UNSET:
            field_dict["username"] = username
        if password is not UNSET:
            field_dict["password"] = password
        if host is not UNSET:
            field_dict["host"] = host
        if port is not UNSET:
            field_dict["port"] = port
        if db_name is not UNSET:
            field_dict["dbName"] = db_name
        if custom_db_url is not UNSET:
            field_dict["customDbUrl"] = custom_db_url
        if db_url is not UNSET:
            field_dict["dbUrl"] = db_url

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        db_type = CreateDbDataSetRequestDbType(d.pop("dbType"))




        query = d.pop("query")

        data_origin = CreateDbDataSetRequestDataOrigin(d.pop("dataOrigin"))




        description = d.pop("description", UNSET)

        username = d.pop("username", UNSET)

        password = d.pop("password", UNSET)

        host = d.pop("host", UNSET)

        port = d.pop("port", UNSET)

        db_name = d.pop("dbName", UNSET)

        custom_db_url = d.pop("customDbUrl", UNSET)

        db_url = d.pop("dbUrl", UNSET)

        create_db_data_set_request = cls(
            name=name,
            db_type=db_type,
            query=query,
            data_origin=data_origin,
            description=description,
            username=username,
            password=password,
            host=host,
            port=port,
            db_name=db_name,
            custom_db_url=custom_db_url,
            db_url=db_url,
        )

        create_db_data_set_request.additional_properties = d
        return create_db_data_set_request

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
