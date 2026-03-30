from src.backend.domain.shared.value_objects.errors import DomainError


class EmailError(DomainError):
    """
    Базовая ошибка VO Email
    """


class InvalidEmailError(EmailError):
    """
    Вызывается когда неправильный формат электронной почты
    """