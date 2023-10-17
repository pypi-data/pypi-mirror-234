from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.sentiment_analysis_step_step_type import SentimentAnalysisStepStepType

T = TypeVar("T", bound="SentimentAnalysisStep")

@attr.s(auto_attribs=True)
class SentimentAnalysisStep:
    """
    Attributes:
        column (str):
        new_sentiment_column_name (str):
        step_type (SentimentAnalysisStepStepType):
    """

    column: str
    new_sentiment_column_name: str
    step_type: SentimentAnalysisStepStepType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        column = self.column
        new_sentiment_column_name = self.new_sentiment_column_name
        step_type = self.step_type.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "column": column,
            "newSentimentColumnName": new_sentiment_column_name,
            "stepType": step_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        column = d.pop("column")

        new_sentiment_column_name = d.pop("newSentimentColumnName")

        step_type = SentimentAnalysisStepStepType(d.pop("stepType"))




        sentiment_analysis_step = cls(
            column=column,
            new_sentiment_column_name=new_sentiment_column_name,
            step_type=step_type,
        )

        sentiment_analysis_step.additional_properties = d
        return sentiment_analysis_step

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
