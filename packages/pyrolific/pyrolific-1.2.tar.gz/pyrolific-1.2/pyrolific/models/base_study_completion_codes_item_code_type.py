from enum import Enum


class BaseStudyCompletionCodesItemCodeType(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED_ATTENTION_CHECK = "FAILED_ATTENTION_CHECK"
    FOLLOW_UP_STUDY = "FOLLOW_UP_STUDY"
    GIVE_BONUS = "GIVE_BONUS"
    INCOMPATIBLE_DEVICE = "INCOMPATIBLE_DEVICE"
    NO_CONSENT = "NO_CONSENT"
    OTHER = "OTHER"

    def __str__(self) -> str:
        return str(self.value)
