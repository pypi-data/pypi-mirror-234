from enum import Enum


class AutomaticallyApproveAction(str, Enum):
    AUTOMATICALLY_APPROVE = "AUTOMATICALLY_APPROVE"

    def __str__(self) -> str:
        return str(self.value)
