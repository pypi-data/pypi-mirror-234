from enum import Enum


class SubscriptionEventStatus(str, Enum):
    FAILED = "FAILED"
    PENDING = "PENDING"
    SUCCEEDED = "SUCCEEDED"

    def __str__(self) -> str:
        return str(self.value)
