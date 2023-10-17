import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.create_auto_clustering_request import CreateAutoClusteringRequest
from ..models.create_classification_request import CreateClassificationRequest
from ..models.create_clustering_request import CreateClusteringRequest
from ..models.create_decisioning_request import CreateDecisioningRequest
from ..models.create_forecasting_request import CreateForecastingRequest
from ..models.create_multi_forecasting_request import CreateMultiForecastingRequest
from ..models.create_regression_request import CreateRegressionRequest
from ..models.model_health import ModelHealth
from ..models.model_influence import ModelInfluence
from ..models.model_score import ModelScore
from ..models.model_status import ModelStatus
from ..models.null_request import NullRequest
from ..models.problem_type import ProblemType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelResponse")

@attr.s(auto_attribs=True)
class ModelResponse:
    """
    Attributes:
        id (int):
        project_id (int):
        name (str):
        created_at (datetime.datetime):
        created_by (str):
        status (ModelStatus):
        problem_type (ProblemType):
        description (Union[Unset, None, str]):
        progress_percent (Optional[float]):
        failure_details (Union[Unset, None, str]):
        model_type (Union[Unset, str]):
        health (Union[Unset, None, ModelHealth]):
        score (Union[Unset, None, ModelScore]):
        influences (Union[Unset, None, List[ModelInfluence]]):
        create_config (Union[CreateAutoClusteringRequest, CreateClassificationRequest, CreateClusteringRequest,
            CreateDecisioningRequest, CreateForecastingRequest, CreateMultiForecastingRequest, CreateRegressionRequest,
            None, NullRequest, Unset]):
        create_endpoint (Union[Unset, str]):
    """

    id: int
    project_id: int
    name: str
    created_at: datetime.datetime
    created_by: str
    status: ModelStatus
    problem_type: ProblemType
    progress_percent: Optional[float]
    description: Union[Unset, None, str] = UNSET
    failure_details: Union[Unset, None, str] = UNSET
    model_type: Union[Unset, str] = UNSET
    health: Union[Unset, None, ModelHealth] = UNSET
    score: Union[Unset, None, ModelScore] = UNSET
    influences: Union[Unset, None, List[ModelInfluence]] = UNSET
    create_config: Union[CreateAutoClusteringRequest, CreateClassificationRequest, CreateClusteringRequest, CreateDecisioningRequest, CreateForecastingRequest, CreateMultiForecastingRequest, CreateRegressionRequest, None, NullRequest, Unset] = UNSET
    create_endpoint: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        project_id = self.project_id
        name = self.name
        created_at = self.created_at.isoformat()

        created_by = self.created_by
        status = self.status.value

        problem_type = self.problem_type.value

        description = self.description
        progress_percent = self.progress_percent
        failure_details = self.failure_details
        model_type = self.model_type
        health: Union[Unset, None, str] = UNSET
        if not isinstance(self.health, Unset):
            health = self.health.value if self.health else None

        score: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.score, Unset):
            score = self.score.to_dict() if self.score else None

        influences: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.influences, Unset):
            if self.influences is None:
                influences = None
            else:
                influences = []
                for influences_item_data in self.influences:
                    influences_item = influences_item_data.to_dict()

                    influences.append(influences_item)




        create_config: Union[Dict[str, Any], None, Unset]
        if isinstance(self.create_config, Unset):
            create_config = UNSET
        elif self.create_config is None:
            create_config = None

        elif isinstance(self.create_config, CreateAutoClusteringRequest):
            create_config = UNSET
            if not isinstance(self.create_config, Unset):
                create_config = self.create_config.to_dict()

        elif isinstance(self.create_config, CreateClassificationRequest):
            create_config = UNSET
            if not isinstance(self.create_config, Unset):
                create_config = self.create_config.to_dict()

        elif isinstance(self.create_config, CreateClusteringRequest):
            create_config = UNSET
            if not isinstance(self.create_config, Unset):
                create_config = self.create_config.to_dict()

        elif isinstance(self.create_config, CreateForecastingRequest):
            create_config = UNSET
            if not isinstance(self.create_config, Unset):
                create_config = self.create_config.to_dict()

        elif isinstance(self.create_config, CreateMultiForecastingRequest):
            create_config = UNSET
            if not isinstance(self.create_config, Unset):
                create_config = self.create_config.to_dict()

        elif isinstance(self.create_config, CreateRegressionRequest):
            create_config = UNSET
            if not isinstance(self.create_config, Unset):
                create_config = self.create_config.to_dict()

        elif isinstance(self.create_config, CreateDecisioningRequest):
            create_config = UNSET
            if not isinstance(self.create_config, Unset):
                create_config = self.create_config.to_dict()

        else:
            create_config = UNSET
            if not isinstance(self.create_config, Unset):
                create_config = self.create_config.to_dict() if self.create_config else None



        create_endpoint = self.create_endpoint

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "projectId": project_id,
            "name": name,
            "createdAt": created_at,
            "createdBy": created_by,
            "status": status,
            "problemType": problem_type,
            "progressPercent": progress_percent,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if failure_details is not UNSET:
            field_dict["failureDetails"] = failure_details
        if model_type is not UNSET:
            field_dict["modelType"] = model_type
        if health is not UNSET:
            field_dict["health"] = health
        if score is not UNSET:
            field_dict["score"] = score
        if influences is not UNSET:
            field_dict["influences"] = influences
        if create_config is not UNSET:
            field_dict["createConfig"] = create_config
        if create_endpoint is not UNSET:
            field_dict["createEndpoint"] = create_endpoint

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        project_id = d.pop("projectId")

        name = d.pop("name")

        created_at = isoparse(d.pop("createdAt"))




        created_by = d.pop("createdBy")

        status = ModelStatus(d.pop("status"))




        problem_type = ProblemType(d.pop("problemType"))




        description = d.pop("description", UNSET)

        progress_percent = d.pop("progressPercent")

        failure_details = d.pop("failureDetails", UNSET)

        model_type = d.pop("modelType", UNSET)

        _health = d.pop("health", UNSET)
        health: Union[Unset, None, ModelHealth]
        if _health is None:
            health = None
        elif isinstance(_health,  Unset):
            health = UNSET
        else:
            health = ModelHealth(_health)




        _score = d.pop("score", UNSET)
        score: Union[Unset, None, ModelScore]
        if _score is None:
            score = None
        elif isinstance(_score,  Unset):
            score = UNSET
        else:
            score = ModelScore.from_dict(_score)




        influences = []
        _influences = d.pop("influences", UNSET)
        for influences_item_data in (_influences or []):
            influences_item = ModelInfluence.from_dict(influences_item_data)



            influences.append(influences_item)


        def _parse_create_config(data: object) -> Union[CreateAutoClusteringRequest, CreateClassificationRequest, CreateClusteringRequest, CreateDecisioningRequest, CreateForecastingRequest, CreateMultiForecastingRequest, CreateRegressionRequest, None, NullRequest, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _create_config_type_0 = data
                create_config_type_0: Union[Unset, CreateAutoClusteringRequest]
                if isinstance(_create_config_type_0,  Unset):
                    create_config_type_0 = UNSET
                else:
                    create_config_type_0 = CreateAutoClusteringRequest.from_dict(_create_config_type_0)



                return create_config_type_0
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _create_config_type_1 = data
                create_config_type_1: Union[Unset, CreateClassificationRequest]
                if isinstance(_create_config_type_1,  Unset):
                    create_config_type_1 = UNSET
                else:
                    create_config_type_1 = CreateClassificationRequest.from_dict(_create_config_type_1)



                return create_config_type_1
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _create_config_type_2 = data
                create_config_type_2: Union[Unset, CreateClusteringRequest]
                if isinstance(_create_config_type_2,  Unset):
                    create_config_type_2 = UNSET
                else:
                    create_config_type_2 = CreateClusteringRequest.from_dict(_create_config_type_2)



                return create_config_type_2
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _create_config_type_3 = data
                create_config_type_3: Union[Unset, CreateForecastingRequest]
                if isinstance(_create_config_type_3,  Unset):
                    create_config_type_3 = UNSET
                else:
                    create_config_type_3 = CreateForecastingRequest.from_dict(_create_config_type_3)



                return create_config_type_3
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _create_config_type_4 = data
                create_config_type_4: Union[Unset, CreateMultiForecastingRequest]
                if isinstance(_create_config_type_4,  Unset):
                    create_config_type_4 = UNSET
                else:
                    create_config_type_4 = CreateMultiForecastingRequest.from_dict(_create_config_type_4)



                return create_config_type_4
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _create_config_type_5 = data
                create_config_type_5: Union[Unset, CreateRegressionRequest]
                if isinstance(_create_config_type_5,  Unset):
                    create_config_type_5 = UNSET
                else:
                    create_config_type_5 = CreateRegressionRequest.from_dict(_create_config_type_5)



                return create_config_type_5
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _create_config_type_6 = data
                create_config_type_6: Union[Unset, CreateDecisioningRequest]
                if isinstance(_create_config_type_6,  Unset):
                    create_config_type_6 = UNSET
                else:
                    create_config_type_6 = CreateDecisioningRequest.from_dict(_create_config_type_6)



                return create_config_type_6
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _create_config_type_7 = data
            create_config_type_7: Union[Unset, None, NullRequest]
            if _create_config_type_7 is None:
                create_config_type_7 = UNSET
            elif isinstance(_create_config_type_7,  Unset):
                create_config_type_7 = UNSET
            else:
                create_config_type_7 = NullRequest.from_dict(_create_config_type_7)



            return create_config_type_7

        create_config = _parse_create_config(d.pop("createConfig", UNSET))


        create_endpoint = d.pop("createEndpoint", UNSET)

        model_response = cls(
            id=id,
            project_id=project_id,
            name=name,
            created_at=created_at,
            created_by=created_by,
            status=status,
            problem_type=problem_type,
            description=description,
            progress_percent=progress_percent,
            failure_details=failure_details,
            model_type=model_type,
            health=health,
            score=score,
            influences=influences,
            create_config=create_config,
            create_endpoint=create_endpoint,
        )

        model_response.additional_properties = d
        return model_response

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
