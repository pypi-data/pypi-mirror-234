from enum import Enum


class NlpLanguage(str, Enum):
    AUTO_DETECT = "AUTO_DETECT"
    ARABIC = "ARABIC"
    DANISH = "DANISH"
    DUTCH = "DUTCH"
    ENGLISH = "ENGLISH"
    FINNISH = "FINNISH"
    FRENCH = "FRENCH"
    GERMAN = "GERMAN"
    HUNGARIAN = "HUNGARIAN"
    ITALIAN = "ITALIAN"
    JAPANESE = "JAPANESE"
    NORWEGIAN = "NORWEGIAN"
    PORTUGUESE = "PORTUGUESE"
    ROMANIAN = "ROMANIAN"
    RUSSIAN = "RUSSIAN"
    SPANISH = "SPANISH"
    SWEDISH = "SWEDISH"
    NONE = "NONE"

    def __str__(self) -> str:
        return str(self.value)