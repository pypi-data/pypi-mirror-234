from enum import Enum


class QuestionType(str, Enum):
    MULTIPLE = "multiple"
    SINGLE = "single"

    def __str__(self) -> str:
        return str(self.value)
