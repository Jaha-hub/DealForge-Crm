from src.backend.domain.shared.value_objects.errors import DomainError


class NameError(DomainError):
    """
    Базовый тип ошибки VO Name
    """

class NameTypeError(NameError):
    """
    Вызывается когда тип имени неправильный
    """

class NameLengthError(NameError):
    """
    Вызывается когда длина имени не в указанном диапазоне
    """

class InvalidNameError(NameError):
    """
    Вызывается когда имя содержит не подходящие символы
    """