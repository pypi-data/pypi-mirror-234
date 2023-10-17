import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.simple_forecast_cadence import SimpleForecastCadence
from ..types import UNSET, Unset

T = TypeVar("T", bound="SimpleForecast")

@attr.s(auto_attribs=True)
class SimpleForecast:
    """
    Attributes:
        horizon (Union[Unset, int]):
        cadence (Union[Unset, SimpleForecastCadence]):
        index (Union[Unset, datetime.datetime]):
        predicted_value (Union[Unset, float]):
        lower_bound (Union[Unset, float]):
        upper_bound (Union[Unset, float]):
        historic_rmse_score (Union[Unset, float]):
        historic_r2_score (Union[Unset, float]):
    """

    horizon: Union[Unset, int] = UNSET
    cadence: Union[Unset, SimpleForecastCadence] = UNSET
    index: Union[Unset, datetime.datetime] = UNSET
    predicted_value: Union[Unset, float] = UNSET
    lower_bound: Union[Unset, float] = UNSET
    upper_bound: Union[Unset, float] = UNSET
    historic_rmse_score: Union[Unset, float] = UNSET
    historic_r2_score: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        horizon = self.horizon
        cadence: Union[Unset, str] = UNSET
        if not isinstance(self.cadence, Unset):
            cadence = self.cadence.value

        index: Union[Unset, str] = UNSET
        if not isinstance(self.index, Unset):
            index = self.index.isoformat()

        predicted_value = self.predicted_value
        lower_bound = self.lower_bound
        upper_bound = self.upper_bound
        historic_rmse_score = self.historic_rmse_score
        historic_r2_score = self.historic_r2_score

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if horizon is not UNSET:
            field_dict["horizon"] = horizon
        if cadence is not UNSET:
            field_dict["cadence"] = cadence
        if index is not UNSET:
            field_dict["index"] = index
        if predicted_value is not UNSET:
            field_dict["predictedValue"] = predicted_value
        if lower_bound is not UNSET:
            field_dict["lowerBound"] = lower_bound
        if upper_bound is not UNSET:
            field_dict["upperBound"] = upper_bound
        if historic_rmse_score is not UNSET:
            field_dict["historicRmseScore"] = historic_rmse_score
        if historic_r2_score is not UNSET:
            field_dict["historicR2Score"] = historic_r2_score

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        horizon = d.pop("horizon", UNSET)

        _cadence = d.pop("cadence", UNSET)
        cadence: Union[Unset, SimpleForecastCadence]
        if isinstance(_cadence,  Unset):
            cadence = UNSET
        else:
            cadence = SimpleForecastCadence(_cadence)




        _index = d.pop("index", UNSET)
        index: Union[Unset, datetime.datetime]
        if isinstance(_index,  Unset):
            index = UNSET
        else:
            index = isoparse(_index)




        predicted_value = d.pop("predictedValue", UNSET)

        lower_bound = d.pop("lowerBound", UNSET)

        upper_bound = d.pop("upperBound", UNSET)

        historic_rmse_score = d.pop("historicRmseScore", UNSET)

        historic_r2_score = d.pop("historicR2Score", UNSET)

        simple_forecast = cls(
            horizon=horizon,
            cadence=cadence,
            index=index,
            predicted_value=predicted_value,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            historic_rmse_score=historic_rmse_score,
            historic_r2_score=historic_r2_score,
        )

        simple_forecast.additional_properties = d
        return simple_forecast

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
