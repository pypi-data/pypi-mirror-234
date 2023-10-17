from enum import Enum


class CreateInvitationRequestRole(str, Enum):
    PROJECT_EDITOR = "PROJECT_EDITOR"
    WORKSPACE_ADMIN = "WORKSPACE_ADMIN"
    WORKSPACE_COLLABORATOR = "WORKSPACE_COLLABORATOR"

    def __str__(self) -> str:
        return str(self.value)
