from dataclasses import dataclass
from datetime import date
from uuid import UUID

from src.backend.domain.lead.value_objects.field_value.errors import EmptyFieldValueError, MultipleFieldValueError


@dataclass(frozen=True)
class FieldValue:
    value_text: str | None = None
    value_number: float | None = None
    value_date: date | None = None
    value_boolean: bool | None = None
    enum_id: UUID | None = None

    def __post_init__(self):
        fields = [
            self.value_text,
            self.value_number,
            self.value_date,
            self.value_boolean,
            self.enum_id
        ]
        filled_fields_count = sum(1 for f in fields if f is not None)
        if filled_fields_count > 1:
            raise EmptyFieldValueError("должно быть заполнено одно поле")
        if filled_fields_count < 1:
            raise MultipleFieldValueError("Хотя бы одно поле должно быть заполнено")