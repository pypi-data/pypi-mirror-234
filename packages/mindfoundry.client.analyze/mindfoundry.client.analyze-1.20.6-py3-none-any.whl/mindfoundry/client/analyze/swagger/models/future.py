from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.future_output_of_your_request import FutureOutputOfYourRequest
from ..models.status import Status
from ..types import UNSET, Unset

T = TypeVar("T", bound="Future")

@attr.s(auto_attribs=True)
class Future:
    """
    Attributes:
        future_id (Union[Unset, str]):
        status (Union[Unset, Status]):
        response (Union[Unset, None, FutureOutputOfYourRequest]):
    """

    future_id: Union[Unset, str] = UNSET
    status: Union[Unset, Status] = UNSET
    response: Union[Unset, None, FutureOutputOfYourRequest] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        future_id = self.future_id
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        response: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.response, Unset):
            response = self.response.to_dict() if self.response else None


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if future_id is not UNSET:
            field_dict["futureId"] = future_id
        if status is not UNSET:
            field_dict["status"] = status
        if response is not UNSET:
            field_dict["response"] = response

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        future_id = d.pop("futureId", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, Status]
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = Status(_status)




        _response = d.pop("response", UNSET)
        response: Union[Unset, None, FutureOutputOfYourRequest]
        if _response is None:
            response = None
        elif isinstance(_response,  Unset):
            response = UNSET
        else:
            response = FutureOutputOfYourRequest.from_dict(_response)




        future = cls(
            future_id=future_id,
            status=status,
            response=response,
        )

        future.additional_properties = d
        return future

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
