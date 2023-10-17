from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.prediction_forecast_response_model_forecasts_item import (
    PredictionForecastResponseModelForecastsItem,
)

T = TypeVar("T", bound="PredictionForecastResponse")

@attr.s(auto_attribs=True)
class PredictionForecastResponse:
    """
    Attributes:
        id (int):
        model_forecasts (List[PredictionForecastResponseModelForecastsItem]):
    """

    id: int
    model_forecasts: List[PredictionForecastResponseModelForecastsItem]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        model_forecasts = []
        for model_forecasts_item_data in self.model_forecasts:
            model_forecasts_item = model_forecasts_item_data.to_dict()

            model_forecasts.append(model_forecasts_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "modelForecasts": model_forecasts,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        model_forecasts = []
        _model_forecasts = d.pop("modelForecasts")
        for model_forecasts_item_data in (_model_forecasts):
            model_forecasts_item = PredictionForecastResponseModelForecastsItem.from_dict(model_forecasts_item_data)



            model_forecasts.append(model_forecasts_item)


        prediction_forecast_response = cls(
            id=id,
            model_forecasts=model_forecasts,
        )

        prediction_forecast_response.additional_properties = d
        return prediction_forecast_response

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
