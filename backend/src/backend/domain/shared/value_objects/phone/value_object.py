import re
from dataclasses import dataclass

from src.backend.domain.shared.value_objects.phone.errors import PhoneFormatError


@dataclass(frozen=True)
class Phone:
    """
    Представляет номер телефона как value object.

    Выполняет валидацию формата номера при создании.

    Attributes:
        value: Номер телефона в строковом формате
    """

    value: str

    def __post_init__(self):
        """
        Выполняет валидацию после создания объекта.

        Raises:
            PhoneFormatError: Если номер телефона имеет некорректный формат
        """
        if not self.__is_valid():
            raise PhoneFormatError

    def __is_valid(self) -> bool:
        """
        Проверяет корректность формата номера телефона.

        Удаляет пробелы, скобки и дефисы перед проверкой.

        Returns:
            True, если номер соответствует международному формату, иначе False
        """
        clean_phone = re.sub(pattern=r'[\s\(\)\-]', repl='', string=self.value)

        # Регулярное выражение:
        # ^\+          - начинается с плюса
        # [1-9]        - первая цифра кода страны (не ноль)
        # \d{1,3}      - еще до 3-х цифр кода страны
        # \d{5,12}     - от 5 до 12 цифр самого номера
        # $            - конец строки
        pattern = r'^\+[1-9]\d{1,3}\d{5,12}$'

        return bool(re.match(pattern, clean_phone))