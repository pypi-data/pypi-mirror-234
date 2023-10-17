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
from ..models.status import Status
from ..models.transform_text_step import TransformTextStep

T = TypeVar("T", bound="DataPrepStepResponse")

@attr.s(auto_attribs=True)
class DataPrepStepResponse:
    """
    Attributes:
        id (int):
        status (Status):
        warning_count (int):
        step (Union[ApplyFormulaStep, CombineStep, DropStep, FillMissingValueStep, FilterRowsStep, GroupByStep,
            MergeColumnsStep, NormalizeTextStep, RenameStep, ReplaceStep, SentimentAnalysisStep, SetColumnLevelStep,
            SetColumnTypeStep, SetTimeIndexStep, SimplifyCategoriesStep, SplitColumnStep, TransformTextStep]):
    """

    id: int
    status: Status
    warning_count: int
    step: Union[ApplyFormulaStep, CombineStep, DropStep, FillMissingValueStep, FilterRowsStep, GroupByStep, MergeColumnsStep, NormalizeTextStep, RenameStep, ReplaceStep, SentimentAnalysisStep, SetColumnLevelStep, SetColumnTypeStep, SetTimeIndexStep, SimplifyCategoriesStep, SplitColumnStep, TransformTextStep]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        status = self.status.value

        warning_count = self.warning_count
        step: Dict[str, Any]

        if isinstance(self.step, ApplyFormulaStep):
            step = self.step.to_dict()

        elif isinstance(self.step, CombineStep):
            step = self.step.to_dict()

        elif isinstance(self.step, DropStep):
            step = self.step.to_dict()

        elif isinstance(self.step, FillMissingValueStep):
            step = self.step.to_dict()

        elif isinstance(self.step, FilterRowsStep):
            step = self.step.to_dict()

        elif isinstance(self.step, GroupByStep):
            step = self.step.to_dict()

        elif isinstance(self.step, MergeColumnsStep):
            step = self.step.to_dict()

        elif isinstance(self.step, NormalizeTextStep):
            step = self.step.to_dict()

        elif isinstance(self.step, RenameStep):
            step = self.step.to_dict()

        elif isinstance(self.step, ReplaceStep):
            step = self.step.to_dict()

        elif isinstance(self.step, SentimentAnalysisStep):
            step = self.step.to_dict()

        elif isinstance(self.step, SetColumnLevelStep):
            step = self.step.to_dict()

        elif isinstance(self.step, SetColumnTypeStep):
            step = self.step.to_dict()

        elif isinstance(self.step, SetTimeIndexStep):
            step = self.step.to_dict()

        elif isinstance(self.step, SimplifyCategoriesStep):
            step = self.step.to_dict()

        elif isinstance(self.step, SplitColumnStep):
            step = self.step.to_dict()

        else:
            step = self.step.to_dict()




        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "status": status,
            "warningCount": warning_count,
            "step": step,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        status = Status(d.pop("status"))




        warning_count = d.pop("warningCount")

        def _parse_step(data: object) -> Union[ApplyFormulaStep, CombineStep, DropStep, FillMissingValueStep, FilterRowsStep, GroupByStep, MergeColumnsStep, NormalizeTextStep, RenameStep, ReplaceStep, SentimentAnalysisStep, SetColumnLevelStep, SetColumnTypeStep, SetTimeIndexStep, SimplifyCategoriesStep, SplitColumnStep, TransformTextStep]:
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

        step = _parse_step(d.pop("step"))


        data_prep_step_response = cls(
            id=id,
            status=status,
            warning_count=warning_count,
            step=step,
        )

        data_prep_step_response.additional_properties = d
        return data_prep_step_response

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
