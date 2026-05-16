import re
from dataclasses import dataclass

from src.backend.domain.shared.value_objects.email.errors import InvalidEmailError


@dataclass(frozen=True)
class Email:
    """
    VO Email нужен для полей в которых будет электронная почта
    """
    value: str

    def __post_init__(self):
        if not self.__is_valid():
            raise InvalidEmailError()

    def __is_valid(self):
        """
        Приватная функция для проверки валидного email
        :return:
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        return re.match(pattern, self.value) is not None

    def __str__(self):
        return self.value