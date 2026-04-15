class DomainError(Exception):
    """
    Базовая Ошибка Domain слоя
    """

class PermissionDeniedError(DomainError):
    pass
