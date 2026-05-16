from src.backend.domain.shared.policy import Policy
from src.backend.domain.user.entity import UserRole, User


class CanManageCustomField(Policy):
    ALLOWED_ROLES = {UserRole.admin,UserRole.director}

    def __init__(self,actor: User):
        self._actor = actor

    def is_satisfied_by(self) -> bool:
        return self._actor.role in self.ALLOWED_ROLES

    def _error_message(self) -> str:
        return "Only admin or director can manage custom fields"