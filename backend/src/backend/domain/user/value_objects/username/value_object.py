import re
from dataclasses import dataclass

from src.backend.application.auth.errors import WeakPasswordError

@dataclass(frozen=True)
class Password:
    """
    VO (Value Object) для пароля пользователя
    Инкапсулирует значение пароля и гарантирует его валидность
    """

    value: str

    def __post_init__(self):
        """
        Вызывается после инициализации объекта.
        Проверяет корректность значения пароля

        Raises:
            WeakPasswordError: если пароль не соответствует требованиям безопасности
        """
        self._validate()

    def _validate(self):
        """
        Выполняет валидацию пароля по следующим правилам:
        - Минимальная длина 8 символов
        - Наличие хотя бы одной заглавной буквы
        - Наличие хотя бы одной строчной буквы
        - Наличие хотя бы одной цифры
        - Наличие хотя бы одного специального символа

        Raises:
            WeakPasswordError: если любое из условий не выполнено
        """
        v = self.value

        if len(v) < 8:
            raise WeakPasswordError("Пароль должен содержать минимум 8 символов")

        if not re.search(r"[A-Z]", v):
            raise WeakPasswordError("Пароль должен содержать хотя бы одну заглавную букву")

        if not re.search(r"[a-z]", v):
            raise WeakPasswordError("Пароль должен содержать хотя бы одну строчную букву")

        if not re.search(r"\d", v):
            raise WeakPasswordError("Пароль должен содержать хотя бы одну цифру")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise WeakPasswordError("Пароль должен содержать хотя бы один специальный символ")

    def is_same_as(self, other: "Password") -> bool:
        """
        Сравнивает текущий пароль с другим

        Args:
            other (Password): другой объект пароля

        Returns:
            bool: True, если пароли совпадают, иначе False
        """
        return self.value == other.value