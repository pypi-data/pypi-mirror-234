from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.classification_model_type import ClassificationModelType
from ..models.classification_scorers import ClassificationScorers
from ..models.data_partition_method import DataPartitionMethod
from ..models.model_validation_method import ModelValidationMethod
from ..models.nlp_language import NlpLanguage
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateClassificationRequest")

@attr.s(auto_attribs=True)
class CreateClassificationRequest:
    """
    Attributes:
        name (str):
        data_set_id (int):
        target_column (str):
        score_to_optimize (ClassificationScorers):
        model_validation_method (ModelValidationMethod):
        data_partition_method (DataPartitionMethod):
        number_of_evaluations (int):
        description (Union[Unset, str]):
        excluded_columns (Union[Unset, List[str]]):
        nlp_language (Union[Unset, NlpLanguage]):  Default: NlpLanguage.AUTO_DETECT.
        draft_mode (Union[Unset, bool]):
        hold_out_percentage (Union[Unset, float]):  Default: 10.0.
        no_mixing_columns (Union[Unset, List[str]]):
        partition_column (Union[Unset, str]):
        order_by_column (Union[Unset, str]):
        weight_column (Union[Unset, str]):
        model_types (Union[Unset, List[ClassificationModelType]]): If omitted - all eligable model types are chosen.
    """

    name: str
    data_set_id: int
    target_column: str
    score_to_optimize: ClassificationScorers
    model_validation_method: ModelValidationMethod
    data_partition_method: DataPartitionMethod
    number_of_evaluations: int
    description: Union[Unset, str] = UNSET
    excluded_columns: Union[Unset, List[str]] = UNSET
    nlp_language: Union[Unset, NlpLanguage] = NlpLanguage.AUTO_DETECT
    draft_mode: Union[Unset, bool] = UNSET
    hold_out_percentage: Union[Unset, float] = 10.0
    no_mixing_columns: Union[Unset, List[str]] = UNSET
    partition_column: Union[Unset, str] = UNSET
    order_by_column: Union[Unset, str] = UNSET
    weight_column: Union[Unset, str] = UNSET
    model_types: Union[Unset, List[ClassificationModelType]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        data_set_id = self.data_set_id
        target_column = self.target_column
        score_to_optimize = self.score_to_optimize.value

        model_validation_method = self.model_validation_method.value

        data_partition_method = self.data_partition_method.value

        number_of_evaluations = self.number_of_evaluations
        description = self.description
        excluded_columns: Union[Unset, List[str]] = UNSET
        if not isinstance(self.excluded_columns, Unset):
            excluded_columns = self.excluded_columns




        nlp_language: Union[Unset, str] = UNSET
        if not isinstance(self.nlp_language, Unset):
            nlp_language = self.nlp_language.value

        draft_mode = self.draft_mode
        hold_out_percentage = self.hold_out_percentage
        no_mixing_columns: Union[Unset, List[str]] = UNSET
        if not isinstance(self.no_mixing_columns, Unset):
            no_mixing_columns = self.no_mixing_columns




        partition_column = self.partition_column
        order_by_column = self.order_by_column
        weight_column = self.weight_column
        model_types: Union[Unset, List[str]] = UNSET
        if not isinstance(self.model_types, Unset):
            model_types = []
            for model_types_item_data in self.model_types:
                model_types_item = model_types_item_data.value

                model_types.append(model_types_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "dataSetId": data_set_id,
            "targetColumn": target_column,
            "scoreToOptimize": score_to_optimize,
            "modelValidationMethod": model_validation_method,
            "dataPartitionMethod": data_partition_method,
            "numberOfEvaluations": number_of_evaluations,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if excluded_columns is not UNSET:
            field_dict["excludedColumns"] = excluded_columns
        if nlp_language is not UNSET:
            field_dict["nlpLanguage"] = nlp_language
        if draft_mode is not UNSET:
            field_dict["draftMode"] = draft_mode
        if hold_out_percentage is not UNSET:
            field_dict["holdOutPercentage"] = hold_out_percentage
        if no_mixing_columns is not UNSET:
            field_dict["noMixingColumns"] = no_mixing_columns
        if partition_column is not UNSET:
            field_dict["partitionColumn"] = partition_column
        if order_by_column is not UNSET:
            field_dict["orderByColumn"] = order_by_column
        if weight_column is not UNSET:
            field_dict["weightColumn"] = weight_column
        if model_types is not UNSET:
            field_dict["modelTypes"] = model_types

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        data_set_id = d.pop("dataSetId")

        target_column = d.pop("targetColumn")

        score_to_optimize = ClassificationScorers(d.pop("scoreToOptimize"))




        model_validation_method = ModelValidationMethod(d.pop("modelValidationMethod"))




        data_partition_method = DataPartitionMethod(d.pop("dataPartitionMethod"))




        number_of_evaluations = d.pop("numberOfEvaluations")

        description = d.pop("description", UNSET)

        excluded_columns = cast(List[str], d.pop("excludedColumns", UNSET))


        _nlp_language = d.pop("nlpLanguage", UNSET)
        nlp_language: Union[Unset, NlpLanguage]
        if isinstance(_nlp_language,  Unset):
            nlp_language = UNSET
        else:
            nlp_language = NlpLanguage(_nlp_language)




        draft_mode = d.pop("draftMode", UNSET)

        hold_out_percentage = d.pop("holdOutPercentage", UNSET)

        no_mixing_columns = cast(List[str], d.pop("noMixingColumns", UNSET))


        partition_column = d.pop("partitionColumn", UNSET)

        order_by_column = d.pop("orderByColumn", UNSET)

        weight_column = d.pop("weightColumn", UNSET)

        model_types = []
        _model_types = d.pop("modelTypes", UNSET)
        for model_types_item_data in (_model_types or []):
            model_types_item = ClassificationModelType(model_types_item_data)



            model_types.append(model_types_item)


        create_classification_request = cls(
            name=name,
            data_set_id=data_set_id,
            target_column=target_column,
            score_to_optimize=score_to_optimize,
            model_validation_method=model_validation_method,
            data_partition_method=data_partition_method,
            number_of_evaluations=number_of_evaluations,
            description=description,
            excluded_columns=excluded_columns,
            nlp_language=nlp_language,
            draft_mode=draft_mode,
            hold_out_percentage=hold_out_percentage,
            no_mixing_columns=no_mixing_columns,
            partition_column=partition_column,
            order_by_column=order_by_column,
            weight_column=weight_column,
            model_types=model_types,
        )

        create_classification_request.additional_properties = d
        return create_classification_request

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
