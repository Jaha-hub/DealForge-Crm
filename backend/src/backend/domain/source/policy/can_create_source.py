from src.backend.domain.user.entity import User


def can_create_source(user: User) -> bool:
    allowed_roles = {User.role.admin, User.role.director}
    return user.role in allowed_roles