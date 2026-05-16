from src.backend.domain.shared.value_objects.errors import DomainError


class NameVOError(DomainError):
    """
    Базовый тип ошибки VO Name
    """

class NameTypeError(NameVOError):
    """
    Вызывается когда тип имени неправильный
    """

class NameLengthError(NameVOError):
    """
    Вызывается когда длина имени не в указанном диапазоне
    """

class InvalidNameError(NameVOError):
    """
    Вызывается когда имя содержит не подходящие символы
    """