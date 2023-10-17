from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.discriminators import Discriminators
from ..models.simple_forecast import SimpleForecast

T = TypeVar("T", bound="PredictionForecastResponseModelForecastsItem")

@attr.s(auto_attribs=True)
class PredictionForecastResponseModelForecastsItem:
    """
    Attributes:
        discriminators (Discriminators):
        simple_forecasts (List[SimpleForecast]):
    """

    discriminators: Discriminators
    simple_forecasts: List[SimpleForecast]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        discriminators = self.discriminators.to_dict()

        simple_forecasts = []
        for simple_forecasts_item_data in self.simple_forecasts:
            simple_forecasts_item = simple_forecasts_item_data.to_dict()

            simple_forecasts.append(simple_forecasts_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "discriminators": discriminators,
            "simpleForecasts": simple_forecasts,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        discriminators = Discriminators.from_dict(d.pop("discriminators"))




        simple_forecasts = []
        _simple_forecasts = d.pop("simpleForecasts")
        for simple_forecasts_item_data in (_simple_forecasts):
            simple_forecasts_item = SimpleForecast.from_dict(simple_forecasts_item_data)



            simple_forecasts.append(simple_forecasts_item)


        prediction_forecast_response_model_forecasts_item = cls(
            discriminators=discriminators,
            simple_forecasts=simple_forecasts,
        )

        prediction_forecast_response_model_forecasts_item.additional_properties = d
        return prediction_forecast_response_model_forecasts_item

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
