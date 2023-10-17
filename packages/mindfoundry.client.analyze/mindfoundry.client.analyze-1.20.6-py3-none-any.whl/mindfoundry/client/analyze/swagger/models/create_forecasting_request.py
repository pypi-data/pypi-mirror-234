from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.cadence import Cadence
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateForecastingRequest")

@attr.s(auto_attribs=True)
class CreateForecastingRequest:
    """
    Attributes:
        name (str):
        data_set_id (int):
        target_column (str):
        time_index_column (str):
        cadence (Cadence):
        horizons (List[int]):
        description (Union[Unset, str]):
        excluded_columns (Union[Unset, List[str]]):
    """

    name: str
    data_set_id: int
    target_column: str
    time_index_column: str
    cadence: Cadence
    horizons: List[int]
    description: Union[Unset, str] = UNSET
    excluded_columns: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        data_set_id = self.data_set_id
        target_column = self.target_column
        time_index_column = self.time_index_column
        cadence = self.cadence.value

        horizons = self.horizons




        description = self.description
        excluded_columns: Union[Unset, List[str]] = UNSET
        if not isinstance(self.excluded_columns, Unset):
            excluded_columns = self.excluded_columns





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "dataSetId": data_set_id,
            "targetColumn": target_column,
            "timeIndexColumn": time_index_column,
            "cadence": cadence,
            "horizons": horizons,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if excluded_columns is not UNSET:
            field_dict["excludedColumns"] = excluded_columns

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        data_set_id = d.pop("dataSetId")

        target_column = d.pop("targetColumn")

        time_index_column = d.pop("timeIndexColumn")

        cadence = Cadence(d.pop("cadence"))




        horizons = cast(List[int], d.pop("horizons"))


        description = d.pop("description", UNSET)

        excluded_columns = cast(List[str], d.pop("excludedColumns", UNSET))


        create_forecasting_request = cls(
            name=name,
            data_set_id=data_set_id,
            target_column=target_column,
            time_index_column=time_index_column,
            cadence=cadence,
            horizons=horizons,
            description=description,
            excluded_columns=excluded_columns,
        )

        create_forecasting_request.additional_properties = d
        return create_forecasting_request

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
