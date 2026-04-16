from src.backend.application.auth.errors import AuthError


class ApplicationError(Exception):
    """
    Базовая ошибка слоя ApplicationError
    """
class BadRequestError(ApplicationError):
    pass

class NotAuthorizedError(AuthError):
    pass

class ConflictError(ApplicationError):
    pass