from enum import Enum


class FilterListAttributesType(str, Enum):
    RANGE = "range"
    SELECT = "select"

    def __str__(self) -> str:
        return str(self.value)
