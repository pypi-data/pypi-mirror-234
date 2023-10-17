from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.prediction_response_problem_type import PredictionResponseProblemType
from ..models.prediction_response_task_status import PredictionResponseTaskStatus
from ..models.status import Status
from ..types import UNSET, Unset

T = TypeVar("T", bound="PredictionResponse")

@attr.s(auto_attribs=True)
class PredictionResponse:
    """
    Attributes:
        id (int):
        name (str):
        problem_type (PredictionResponseProblemType):
        task_status (PredictionResponseTaskStatus):
        description (Union[Unset, None, str]):
        project_id (Union[Unset, None, int]):
        model_id (Union[Unset, None, int]):
        data_set_id (Union[Unset, None, int]):
        is_multi_series (Union[Unset, None, bool]):
        status (Union[Unset, Status]):
        failure_details (Union[Unset, None, str]):
        prediction_column_name (Union[Unset, None, str]):
    """

    id: int
    name: str
    problem_type: PredictionResponseProblemType
    task_status: PredictionResponseTaskStatus
    description: Union[Unset, None, str] = UNSET
    project_id: Union[Unset, None, int] = UNSET
    model_id: Union[Unset, None, int] = UNSET
    data_set_id: Union[Unset, None, int] = UNSET
    is_multi_series: Union[Unset, None, bool] = UNSET
    status: Union[Unset, Status] = UNSET
    failure_details: Union[Unset, None, str] = UNSET
    prediction_column_name: Union[Unset, None, str] = UNSET
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
        is_multi_series = self.is_multi_series
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        failure_details = self.failure_details
        prediction_column_name = self.prediction_column_name

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
        if is_multi_series is not UNSET:
            field_dict["isMultiSeries"] = is_multi_series
        if status is not UNSET:
            field_dict["status"] = status
        if failure_details is not UNSET:
            field_dict["failureDetails"] = failure_details
        if prediction_column_name is not UNSET:
            field_dict["predictionColumnName"] = prediction_column_name

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        problem_type = PredictionResponseProblemType(d.pop("problemType"))




        task_status = PredictionResponseTaskStatus(d.pop("taskStatus"))




        description = d.pop("description", UNSET)

        project_id = d.pop("projectId", UNSET)

        model_id = d.pop("modelId", UNSET)

        data_set_id = d.pop("dataSetId", UNSET)

        is_multi_series = d.pop("isMultiSeries", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, Status]
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = Status(_status)




        failure_details = d.pop("failureDetails", UNSET)

        prediction_column_name = d.pop("predictionColumnName", UNSET)

        prediction_response = cls(
            id=id,
            name=name,
            problem_type=problem_type,
            task_status=task_status,
            description=description,
            project_id=project_id,
            model_id=model_id,
            data_set_id=data_set_id,
            is_multi_series=is_multi_series,
            status=status,
            failure_details=failure_details,
            prediction_column_name=prediction_column_name,
        )

        prediction_response.additional_properties = d
        return prediction_response

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
