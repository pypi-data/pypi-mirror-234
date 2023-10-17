from enum import Enum


class InvitationStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    INVITED = "INVITED"

    def __str__(self) -> str:
        return str(self.value)
