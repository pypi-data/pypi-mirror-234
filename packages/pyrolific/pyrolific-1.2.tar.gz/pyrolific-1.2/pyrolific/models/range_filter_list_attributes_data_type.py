from enum import Enum


class RangeFilterListAttributesDataType(str, Enum):
    DATE = "date"
    INTEGER = "integer"

    def __str__(self) -> str:
        return str(self.value)
