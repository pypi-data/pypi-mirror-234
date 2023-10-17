from enum import Enum


class RemoveFromParticipantGroupAction(str, Enum):
    REMOVE_FROM_PARTICIPANT_GROUP = "REMOVE_FROM_PARTICIPANT_GROUP"

    def __str__(self) -> str:
        return str(self.value)
