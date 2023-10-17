from enum import Enum


class SubmissionTransitionRejectionCategory(str, Enum):
    BAD_CODE = "BAD_CODE"
    FAILED_CHECK = "FAILED_CHECK"
    FAILED_INSTRUCTIONS = "FAILED_INSTRUCTIONS"
    INCOMP_LONGITUDINAL = "INCOMP_LONGITUDINAL"
    LOW_EFFORT = "LOW_EFFORT"
    MALINGERING = "MALINGERING"
    NO_CODE = "NO_CODE"
    NO_DATA = "NO_DATA"
    OTHER = "OTHER"
    TOO_QUICKLY = "TOO_QUICKLY"
    TOO_SLOWLY = "TOO_SLOWLY"
    UNSUPP_DEVICE = "UNSUPP_DEVICE"

    def __str__(self) -> str:
        return str(self.value)
