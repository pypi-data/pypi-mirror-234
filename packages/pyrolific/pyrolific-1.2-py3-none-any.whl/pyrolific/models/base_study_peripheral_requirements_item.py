from enum import Enum


class BaseStudyPeripheralRequirementsItem(str, Enum):
    AUDIO = "audio"
    CAMERA = "camera"
    DOWNLOAD = "download"
    MICROPHONE = "microphone"

    def __str__(self) -> str:
        return str(self.value)
