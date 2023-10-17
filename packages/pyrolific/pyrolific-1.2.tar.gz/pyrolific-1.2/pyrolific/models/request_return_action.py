from enum import Enum


class RequestReturnAction(str, Enum):
    REQUEST_RETURN = "REQUEST_RETURN"

    def __str__(self) -> str:
        return str(self.value)
