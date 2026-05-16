from src.backend.domain.user.entity import User, UserRole


class Source:

    def can_update(self, user: User) -> bool:
        if not user.is_active:
            return False

        if user.role == UserRole.admin:
            return True

        return self.owner_id == user.id and not self.is_deleted

    def can_delete(self, user: User) -> bool:
        if not user.is_active:
            return False

        return user.role == UserRole.admin and not self.is_deleted