from enum import Enum


class ManuallyReviewAction(str, Enum):
    MANUALLY_REVIEW = "MANUALLY_REVIEW"

    def __str__(self) -> str:
        return str(self.value)
