from enum import Enum


class BaseStudyCompletionOption(str, Enum):
    CODE = "code"
    URL = "url"

    def __str__(self) -> str:
        return str(self.value)
