from src.backend.domain.shared.policy import Policy
from src.backend.domain.user.entity import UserRole, User


class CanDeleteFunnelPolicy(Policy):
    ALLOWED_ROLES = {UserRole.admin, UserRole.director}

    def __init__(self, actor: User):
        self._actor = actor

    def _error_message(self) -> str:
        return "You can't delete funnel"

    def is_satisfied_by(self) -> bool:
        return self._actor.role in self.ALLOWED_ROLES