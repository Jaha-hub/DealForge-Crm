from src.backend.application.shared.errors import ApplicationError, NotAuthorizedError, BadRequestError


class AuthError(ApplicationError):
    """
    Базовая ошибка Auth
    """


class AuthUserNotFoundError(NotAuthorizedError,AuthError):
    """

    """

class InvalidPasswordError(NotAuthorizedError,AuthError):
    pass

class InactiveUserError(NotAuthorizedError,AuthError):
    pass

class WeakPasswordError(BadRequestError,AuthError):
    pass

class SamePasswordError(BadRequestError,AuthError):
    pass


class EmailAlreadyExistsError(BadRequestError,AuthError):
    pass