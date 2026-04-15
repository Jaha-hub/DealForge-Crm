from src.backend.domain.shared.policy import Policy
from src.backend.domain.user.entity import UserRole, User
from uuid import UUID


class CanUpdateUserPolicy(Policy):
    ALLOWED_ROLES = {UserRole.admin, UserRole.director}

    def __init__(
        self,
        actor: User,
        user_id: UUID,
    ):
        self._actor = actor
        self._user_id = user_id

    def is_satisfied_by(self) -> bool:
        is_self = self._actor.id == self._user_id
        is_privileged = self._actor.role in self.ALLOWED_ROLES
        return is_self or is_privileged