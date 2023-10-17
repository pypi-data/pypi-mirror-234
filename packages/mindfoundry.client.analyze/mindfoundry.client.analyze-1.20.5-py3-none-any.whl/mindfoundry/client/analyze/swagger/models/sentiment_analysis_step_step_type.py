from enum import Enum


class SentimentAnalysisStepStepType(str, Enum):
    SENTIMENT = "sentiment"

    def __str__(self) -> str:
        return str(self.value)