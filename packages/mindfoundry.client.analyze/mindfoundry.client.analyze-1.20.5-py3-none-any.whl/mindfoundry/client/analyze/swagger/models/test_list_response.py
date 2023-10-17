from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.test_response import TestResponse
from ..types import UNSET, Unset

T = TypeVar("T", bound="TestListResponse")

@attr.s(auto_attribs=True)
class TestListResponse:
    """
    Attributes:
        tests (Union[Unset, List[TestResponse]]):
    """

    tests: Union[Unset, List[TestResponse]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        tests: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.tests, Unset):
            tests = []
            for tests_item_data in self.tests:
                tests_item = tests_item_data.to_dict()

                tests.append(tests_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if tests is not UNSET:
            field_dict["tests"] = tests

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tests = []
        _tests = d.pop("tests", UNSET)
        for tests_item_data in (_tests or []):
            tests_item = TestResponse.from_dict(tests_item_data)



            tests.append(tests_item)


        test_list_response = cls(
            tests=tests,
        )

        test_list_response.additional_properties = d
        return test_list_response

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
