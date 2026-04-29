from dataclasses import dataclass

from src.backend.domain.lead.value_objects.contact.errors import ContactError
from src.backend.domain.shared.value_objects.email.value_object import Email
from src.backend.domain.shared.value_objects.name.value_object import Name
from src.backend.domain.shared.value_objects.phone.value_object import Phone


@dataclass(frozen=True)
class Contact:
    fullname: Name
    email: Email | None = None
    phone: Phone | None = None
    telegram: str | None = None

    def __post_init__(self):
        if not (self.email or not self.phone or not self.telegram):
            raise ContactError("Either email or phone or telegram required")
