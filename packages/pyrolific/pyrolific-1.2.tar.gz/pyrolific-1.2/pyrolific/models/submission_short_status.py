from enum import Enum


class SubmissionShortStatus(str, Enum):
    ACTIVE = "ACTIVE"
    APPROVED = "APPROVED"
    AWAITING_REVIEW = "AWAITING REVIEW"
    REJECTED = "REJECTED"
    RESERVED = "RESERVED"
    RETURNED = "RETURNED"
    TIME_OUT = "TIME-OUT"

    def __str__(self) -> str:
        return str(self.value)
