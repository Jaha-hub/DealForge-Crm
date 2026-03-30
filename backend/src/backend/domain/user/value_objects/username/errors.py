from src.backend.domain.shared.value_objects.errors import DomainError


class UsernameError(DomainError):
    """
    Это базовая ошибка VO Username
    """

class UnsupportedUsernameTypeError(UsernameError):
    """
    Вызывается когда неправильный тип значения
    """

class InvalidUsernameLengthError(UsernameError):
    """
    Вызывается когда длина имени пользователя превышает диапазон
    """

class InvalidUsernameFormatError(UsernameError):
    """
    Вызывается когда формат имени пользователя неправильный
    """