import re
from dataclasses import dataclass

from src.backend.domain.shared.value_objects.name.errors import NameTypeError, NameLengthError, InvalidNameError


@dataclass(frozen=True)
class Name:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise NameTypeError()

        if not (2 <= len(self.value) <= 255):
            raise NameLengthError()

        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ]+$', self.value):
            raise InvalidNameError()

    def __is_valid(self) -> bool:
        """
        Приватная функция для проверки валидного имени
        :return: True или False
        """
        pattern = r'^[a-zA-Zа-яА-ЯёЁ]+$'
        return re.match(pattern, self.value) is not None

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return str(self.value)