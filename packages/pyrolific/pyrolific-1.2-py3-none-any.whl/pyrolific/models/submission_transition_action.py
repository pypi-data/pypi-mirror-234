from enum import Enum


class SubmissionTransitionAction(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"

    def __str__(self) -> str:
        return str(self.value)
