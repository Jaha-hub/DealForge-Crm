import re
from dataclasses import dataclass

from src.backend.domain.user.value_objects.username.errors import (
    UnsupportedUsernameTypeError,
    InvalidUsernameLengthError,
    InvalidUsernameFormatError
)


@dataclass(frozen=True)
class Username:
    """
    VO Username

    Attributes:
        value: значение юзернейма
    """
    value: str

    def __post_init__(self):
        """
        Проверяет правильность значения

        Raises:
            UnSupportedUsernameTypeError: если тип не str
            InvalidUsernameLengthError: если длина юзернейма не находится в нужном диапозоне
            InvalidUsernameFormatError: если указан формат юзернейма
        """
        # Проверка Типа Данных
        if not isinstance(self.value, str):
            raise UnsupportedUsernameTypeError()

        # Проверка длины
        if len(self.value) < 3 or len(self.value) > 255:
            raise InvalidUsernameLengthError()

        # Проверка формата
        if not self.__is_valid():
            raise InvalidUsernameFormatError()

        object.__setattr__(self, 'value', self.value.lower())

    def __is_valid(self) -> bool:
        """
        Проверяет правильность формата указанного значения

        Returns:
            True если формат правильный
        """
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
        return re.match(pattern, self.value) is not None

    def __str__(self):
        return self.value
