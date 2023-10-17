from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.apply_formula_step import ApplyFormulaStep
from ..models.combine_step import CombineStep
from ..models.drop_step import DropStep
from ..models.fill_missing_value_step import FillMissingValueStep
from ..models.filter_rows_step import FilterRowsStep
from ..models.group_by_step import GroupByStep
from ..models.merge_columns_step import MergeColumnsStep
from ..models.normalize_text_step import NormalizeTextStep
from ..models.rename_step import RenameStep
from ..models.replace_step import ReplaceStep
from ..models.sentiment_analysis_step import SentimentAnalysisStep
from ..models.set_column_level_step import SetColumnLevelStep
from ..models.set_column_type_step import SetColumnTypeStep
from ..models.set_time_index_step import SetTimeIndexStep
from ..models.simplify_categories_step import SimplifyCategoriesStep
from ..models.split_column_step import SplitColumnStep
from ..models.transform_text_step import TransformTextStep
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApplyDataPrepStepsRequest")

@attr.s(auto_attribs=True)
class ApplyDataPrepStepsRequest:
    """
    Attributes:
        saved_steps_id (Union[Unset, float]): Id of the data prep pipeline to apply to the data set. Must define either
            'savedStepsId' or 'steps'.
        steps (Union[Unset, List[Union[ApplyFormulaStep, CombineStep, DropStep, FillMissingValueStep, FilterRowsStep,
            GroupByStep, MergeColumnsStep, NormalizeTextStep, RenameStep, ReplaceStep, SentimentAnalysisStep,
            SetColumnLevelStep, SetColumnTypeStep, SetTimeIndexStep, SimplifyCategoriesStep, SplitColumnStep,
            TransformTextStep]]]): List of step configurations to apply to the data set. Must define either 'savedStepsId'
            or 'steps'.
        insertion_index (Union[Unset, float]): 0-based index of location in the data set's existing pipeline where the
            steps should be inserted. The steps will be appended to the end if no value is given.
    """

    saved_steps_id: Union[Unset, float] = UNSET
    steps: Union[Unset, List[Union[ApplyFormulaStep, CombineStep, DropStep, FillMissingValueStep, FilterRowsStep, GroupByStep, MergeColumnsStep, NormalizeTextStep, RenameStep, ReplaceStep, SentimentAnalysisStep, SetColumnLevelStep, SetColumnTypeStep, SetTimeIndexStep, SimplifyCategoriesStep, SplitColumnStep, TransformTextStep]]] = UNSET
    insertion_index: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        saved_steps_id = self.saved_steps_id
        steps: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.steps, Unset):
            steps = []
            for steps_item_data in self.steps:
                steps_item: Dict[str, Any]

                if isinstance(steps_item_data, ApplyFormulaStep):
                    steps_item = steps_item_data.to_dict()

                elif isinstance(steps_item_data, CombineStep):
                    steps_item = steps_item_data.to_dict()

                elif isinstance(steps_item_data, DropStep):
                    steps_item = steps_item_data.to_dict()

                elif isinstance(steps_item_data, FillMissingValueStep):
                    steps_item = steps_item_data.to_dict()

                elif isinstance(steps_item_data, FilterRowsStep):
                    steps_item = steps_item_data.to_dict()

                elif isinstance(steps_item_data, GroupByStep):
                    steps_item = steps_item_data.to_dict()

                elif isinstance(steps_item_data, MergeColumnsStep):
                    steps_item = steps_item_data.to_dict()

                elif isinstance(steps_item_data, NormalizeTextStep):
                    steps_item = steps_item_data.to_dict()

                elif isinstance(steps_item_data, RenameStep):
                    steps_item = steps_item_data.to_dict()

                elif isinstance(steps_item_data, ReplaceStep):
                    steps_item = steps_item_data.to_dict()

                elif isinstance(steps_item_data, SentimentAnalysisStep):
                    steps_item = steps_item_data.to_dict()

                elif isinstance(steps_item_data, SetColumnLevelStep):
                    steps_item = steps_item_data.to_dict()

                elif isinstance(steps_item_data, SetColumnTypeStep):
                    steps_item = steps_item_data.to_dict()

                elif isinstance(steps_item_data, SetTimeIndexStep):
                    steps_item = steps_item_data.to_dict()

                elif isinstance(steps_item_data, SimplifyCategoriesStep):
                    steps_item = steps_item_data.to_dict()

                elif isinstance(steps_item_data, SplitColumnStep):
                    steps_item = steps_item_data.to_dict()

                else:
                    steps_item = steps_item_data.to_dict()



                steps.append(steps_item)




        insertion_index = self.insertion_index

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if saved_steps_id is not UNSET:
            field_dict["savedStepsId"] = saved_steps_id
        if steps is not UNSET:
            field_dict["steps"] = steps
        if insertion_index is not UNSET:
            field_dict["insertionIndex"] = insertion_index

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        saved_steps_id = d.pop("savedStepsId", UNSET)

        steps = []
        _steps = d.pop("steps", UNSET)
        for steps_item_data in (_steps or []):
            def _parse_steps_item(data: object) -> Union[ApplyFormulaStep, CombineStep, DropStep, FillMissingValueStep, FilterRowsStep, GroupByStep, MergeColumnsStep, NormalizeTextStep, RenameStep, ReplaceStep, SentimentAnalysisStep, SetColumnLevelStep, SetColumnTypeStep, SetTimeIndexStep, SimplifyCategoriesStep, SplitColumnStep, TransformTextStep]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_data_prep_step_type_0 = ApplyFormulaStep.from_dict(data)



                    return componentsschemas_data_prep_step_type_0
                except: # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_data_prep_step_type_1 = CombineStep.from_dict(data)



                    return componentsschemas_data_prep_step_type_1
                except: # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_data_prep_step_type_2 = DropStep.from_dict(data)



                    return componentsschemas_data_prep_step_type_2
                except: # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_data_prep_step_type_3 = FillMissingValueStep.from_dict(data)



                    return componentsschemas_data_prep_step_type_3
                except: # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_data_prep_step_type_4 = FilterRowsStep.from_dict(data)



                    return componentsschemas_data_prep_step_type_4
                except: # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_data_prep_step_type_5 = GroupByStep.from_dict(data)



                    return componentsschemas_data_prep_step_type_5
                except: # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_data_prep_step_type_6 = MergeColumnsStep.from_dict(data)



                    return componentsschemas_data_prep_step_type_6
                except: # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_data_prep_step_type_7 = NormalizeTextStep.from_dict(data)



                    return componentsschemas_data_prep_step_type_7
                except: # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_data_prep_step_type_8 = RenameStep.from_dict(data)



                    return componentsschemas_data_prep_step_type_8
                except: # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_data_prep_step_type_9 = ReplaceStep.from_dict(data)



                    return componentsschemas_data_prep_step_type_9
                except: # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_data_prep_step_type_10 = SentimentAnalysisStep.from_dict(data)



                    return componentsschemas_data_prep_step_type_10
                except: # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_data_prep_step_type_11 = SetColumnLevelStep.from_dict(data)



                    return componentsschemas_data_prep_step_type_11
                except: # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_data_prep_step_type_12 = SetColumnTypeStep.from_dict(data)



                    return componentsschemas_data_prep_step_type_12
                except: # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_data_prep_step_type_13 = SetTimeIndexStep.from_dict(data)



                    return componentsschemas_data_prep_step_type_13
                except: # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_data_prep_step_type_14 = SimplifyCategoriesStep.from_dict(data)



                    return componentsschemas_data_prep_step_type_14
                except: # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_data_prep_step_type_15 = SplitColumnStep.from_dict(data)



                    return componentsschemas_data_prep_step_type_15
                except: # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_data_prep_step_type_16 = TransformTextStep.from_dict(data)



                return componentsschemas_data_prep_step_type_16

            steps_item = _parse_steps_item(steps_item_data)

            steps.append(steps_item)


        insertion_index = d.pop("insertionIndex", UNSET)

        apply_data_prep_steps_request = cls(
            saved_steps_id=saved_steps_id,
            steps=steps,
            insertion_index=insertion_index,
        )

        apply_data_prep_steps_request.additional_properties = d
        return apply_data_prep_steps_request

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
