from src.backend.domain.shared.errors import DomainError


class UserNotFoundError(DomainError):
    pass


class UsernameAlreadyExistsError(DomainError):
    pass


class EmailAlreadyExistsError(DomainError):
    pass