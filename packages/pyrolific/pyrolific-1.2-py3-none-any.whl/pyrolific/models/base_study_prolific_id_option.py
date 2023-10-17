from enum import Enum


class BaseStudyProlificIdOption(str, Enum):
    NOT_REQUIRED = "not_required"
    QUESTION = "question"
    URL_PARAMETERS = "url_parameters"

    def __str__(self) -> str:
        return str(self.value)
