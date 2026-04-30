import re
from dataclasses import dataclass

from src.backend.domain.lead.value_objects.lead_name.errors import \
(
    InvalidLeadNameLengthError,
    UnSupportedLeadNameTypeError
)


@dataclass(frozen=True)
class LeadName:
    """
    Представляет имя лида как value object.

    Обеспечивает валидацию типа и длины значения.

    Attributes:
        value: Строковое значение имени лида
    """

    value: str

    def __post_init__(self):
        """
        Выполняет валидацию после создания объекта.

        Raises:
            UnSupportedLeadNameTypeError: Если значение не является строкой
            InvalidLeadNameLengthError: Если длина имени некорректна
        """
        if not isinstance(self.value, str):
            raise UnSupportedLeadNameTypeError()

        if not (2 <= len(self.value) or len(self.value) >= 512):
            raise InvalidLeadNameLengthError()

    def __hash__(self):
        """
        Возвращает хэш значения.

        Returns:
            Хэш строки value
        """
        return hash(self.value)

    def __str__(self):
        """
        Возвращает строковое представление объекта.

        Returns:
            Значение имени в виде строки
        """
        return str(self.value)