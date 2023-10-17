from enum import Enum


class StudyShortStudyType(str, Enum):
    SINGLE = "SINGLE"
    UK_REP_SAMPLE = "UK_REP_SAMPLE"
    US_REP_SAMPLE = "US_REP_SAMPLE"

    def __str__(self) -> str:
        return str(self.value)
