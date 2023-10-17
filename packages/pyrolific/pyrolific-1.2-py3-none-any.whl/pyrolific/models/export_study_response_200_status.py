from enum import Enum


class ExportStudyResponse200Status(str, Enum):
    YOUR_EXPORT_SHOULD_ARRIVE_SHORTLY = "Your export should arrive shortly."

    def __str__(self) -> str:
        return str(self.value)
