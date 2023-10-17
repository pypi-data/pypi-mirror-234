from enum import Enum


class SelectFilterListAttributesDataType(str, Enum):
    CHOICEID = "ChoiceID"
    PARTICIPANTGROUPID = "ParticipantGroupID"
    PARTICIPANTID = "ParticipantID"
    STUDYID = "StudyID"

    def __str__(self) -> str:
        return str(self.value)
