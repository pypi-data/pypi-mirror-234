from enum import Enum


class ExportStudyMethod(str, Enum):
    EMAIL = "EMAIL"

    def __str__(self) -> str:
        return str(self.value)
