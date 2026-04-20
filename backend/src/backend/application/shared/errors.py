class ApplicationError(Exception):
    """
    Базовая ошибка слоя ApplicationError
    """
class BadRequestError(ApplicationError):
    pass

class NotAuthorizedError(ApplicationError):
    pass

class ConflictError(ApplicationError):
    pass