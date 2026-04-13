from src.backend.domain.shared.policy import Policy
from src.backend.domain.user.entity import UserRole, User


class CanDeleteUserPolicy(Policy):
    ALLOWED_ROLES = {UserRole.admin, UserRole.director}

    def __init__(self, actor: User, target: User):
        self._actor = actor
        self._target = target

    def is_satisfied_by(self) -> bool:
        if self._actor.role not in self.ALLOWED_ROLES:
            return False

        if self._actor.role == UserRole.director and self._target.role == UserRole.admin:
            return False

        return True

    def _error_message(self) -> str:
        return f"User {self._actor.role} cannot delete {self._target.role}"