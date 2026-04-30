from dataclasses import dataclass

from src.backend.domain.lead.value_objects.contact.errors import ContactError
from src.backend.domain.shared.value_objects.email.value_object import Email
from src.backend.domain.shared.value_objects.name.value_object import Name
from src.backend.domain.shared.value_objects.phone.value_object import Phone


@dataclass(frozen=True)
class Contact:
    """
    Представляет контактную информацию лида.

    Объект является неизменяемым после создания.

    Attributes:
        fullname: Полное имя
        email: Электронная почта
        phone: Номер телефона
        telegram: Telegram username или идентификатор
    """

    fullname: Name
    email: Email | None = None
    phone: Phone | None = None
    telegram: str | None = None

    def __post_init__(self):
        """
        Выполняет валидацию после создания объекта.

        Raises:
            ContactError: Если не указано ни одного способа связи
        """
        if not (self.email or not self.phone or not self.telegram):
            raise ContactError("Either email or phone or telegram required")