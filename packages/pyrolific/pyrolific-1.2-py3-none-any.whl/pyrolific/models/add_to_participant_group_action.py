from enum import Enum


class AddToParticipantGroupAction(str, Enum):
    ADD_TO_PARTICIPANT_GROUP = "ADD_TO_PARTICIPANT_GROUP"

    def __str__(self) -> str:
        return str(self.value)
