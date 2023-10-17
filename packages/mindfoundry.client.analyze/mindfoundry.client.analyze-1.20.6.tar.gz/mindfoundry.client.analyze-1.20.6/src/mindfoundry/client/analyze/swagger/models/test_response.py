from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.model_score import ModelScore
from ..models.status import Status
from ..models.test_response_problem_type import TestResponseProblemType
from ..models.test_response_task_status import TestResponseTaskStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="TestResponse")

@attr.s(auto_attribs=True)
class TestResponse:
    """
    Attributes:
        id (int):
        name (str):
        problem_type (TestResponseProblemType):
        task_status (TestResponseTaskStatus):
        description (Union[Unset, None, str]):
        project_id (Union[Unset, None, int]):
        model_id (Union[Unset, None, int]):
        data_set_id (Union[Unset, None, int]):
        status (Union[Unset, Status]):
        failure_details (Union[Unset, None, str]):
        target_column_name (Union[Unset, None, str]):
        predicted_column_name (Union[Unset, None, str]):
        score (Union[Unset, None, ModelScore]):
    """

    id: int
    name: str
    problem_type: TestResponseProblemType
    task_status: TestResponseTaskStatus
    description: Union[Unset, None, str] = UNSET
    project_id: Union[Unset, None, int] = UNSET
    model_id: Union[Unset, None, int] = UNSET
    data_set_id: Union[Unset, None, int] = UNSET
    status: Union[Unset, Status] = UNSET
    failure_details: Union[Unset, None, str] = UNSET
    target_column_name: Union[Unset, None, str] = UNSET
    predicted_column_name: Union[Unset, None, str] = UNSET
    score: Union[Unset, None, ModelScore] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        problem_type = self.problem_type.value

        task_status = self.task_status.value

        description = self.description
        project_id = self.project_id
        model_id = self.model_id
        data_set_id = self.data_set_id
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        failure_details = self.failure_details
        target_column_name = self.target_column_name
        predicted_column_name = self.predicted_column_name
        score: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.score, Unset):
            score = self.score.to_dict() if self.score else None


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "name": name,
            "problemType": problem_type,
            "taskStatus": task_status,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if model_id is not UNSET:
            field_dict["modelId"] = model_id
        if data_set_id is not UNSET:
            field_dict["dataSetId"] = data_set_id
        if status is not UNSET:
            field_dict["status"] = status
        if failure_details is not UNSET:
            field_dict["failureDetails"] = failure_details
        if target_column_name is not UNSET:
            field_dict["targetColumnName"] = target_column_name
        if predicted_column_name is not UNSET:
            field_dict["predictedColumnName"] = predicted_column_name
        if score is not UNSET:
            field_dict["score"] = score

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        problem_type = TestResponseProblemType(d.pop("problemType"))




        task_status = TestResponseTaskStatus(d.pop("taskStatus"))




        description = d.pop("description", UNSET)

        project_id = d.pop("projectId", UNSET)

        model_id = d.pop("modelId", UNSET)

        data_set_id = d.pop("dataSetId", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, Status]
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = Status(_status)




        failure_details = d.pop("failureDetails", UNSET)

        target_column_name = d.pop("targetColumnName", UNSET)

        predicted_column_name = d.pop("predictedColumnName", UNSET)

        _score = d.pop("score", UNSET)
        score: Union[Unset, None, ModelScore]
        if _score is None:
            score = None
        elif isinstance(_score,  Unset):
            score = UNSET
        else:
            score = ModelScore.from_dict(_score)




        test_response = cls(
            id=id,
            name=name,
            problem_type=problem_type,
            task_status=task_status,
            description=description,
            project_id=project_id,
            model_id=model_id,
            data_set_id=data_set_id,
            status=status,
            failure_details=failure_details,
            target_column_name=target_column_name,
            predicted_column_name=predicted_column_name,
            score=score,
        )

        test_response.additional_properties = d
        return test_response

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
