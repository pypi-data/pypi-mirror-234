from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.prediction_response import PredictionResponse
from ..types import UNSET, Unset

T = TypeVar("T", bound="PredictionListResponse")

@attr.s(auto_attribs=True)
class PredictionListResponse:
    """
    Attributes:
        predictions (Union[Unset, List[PredictionResponse]]):
    """

    predictions: Union[Unset, List[PredictionResponse]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        predictions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.predictions, Unset):
            predictions = []
            for predictions_item_data in self.predictions:
                predictions_item = predictions_item_data.to_dict()

                predictions.append(predictions_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if predictions is not UNSET:
            field_dict["predictions"] = predictions

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        predictions = []
        _predictions = d.pop("predictions", UNSET)
        for predictions_item_data in (_predictions or []):
            predictions_item = PredictionResponse.from_dict(predictions_item_data)



            predictions.append(predictions_item)


        prediction_list_response = cls(
            predictions=predictions,
        )

        prediction_list_response.additional_properties = d
        return prediction_list_response

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
