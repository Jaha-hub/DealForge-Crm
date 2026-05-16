from dataclasses import dataclass

from src.backend.domain.shared.policy import Policy
from src.backend.domain.user.entity import User, UserRole

@dataclass
class CanCreateFunnelPolicy(Policy):
    ALLOW_ROLES = {UserRole.admin, UserRole.director}

    def __init__(self, actor: User):
        self._actor = actor

    def _error_message(self) -> str:
        return "You can't create funnel"

    def is_satisfied_by(self) -> bool:
        return self._actor.role in self.ALLOW_ROLES