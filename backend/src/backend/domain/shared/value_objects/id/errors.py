from src.backend.domain.shared.value_objects.errors import DomainError


class IDError(DomainError):
    """
    Это базовая ошибка VO Id
    """

class UnsupportedTypeIdError(IDError):
    """
    Не поддерживаемый тип значение
    """

class NegativeIntIdError(IDError):
    """
    Вызываются когда дают отрицательное значение
    """