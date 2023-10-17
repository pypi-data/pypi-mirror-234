from enum import Enum


class GetStudiesState(str, Enum):
    ACTIVE = "ACTIVE"
    AWAITING_REVIEW = "AWAITING REVIEW"
    COMPLETED = "COMPLETED"
    PAUSED = "PAUSED"
    PUBLISHING = "PUBLISHING"
    SCHEDULED = "SCHEDULED"
    UNKNOWN = "UNKNOWN"
    UNPUBLISHED = "UNPUBLISHED"

    def __str__(self) -> str:
        return str(self.value)
