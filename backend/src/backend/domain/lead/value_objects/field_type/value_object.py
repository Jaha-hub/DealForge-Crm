from enum import StrEnum

from src.backend.domain.lead.value_objects.field_value.value_objects import FieldValue


class FieldType(StrEnum):
    text = "text"
    number = "number"
    datetime = "date"
    select_one = "select_one"
    select_many = "select_many"
    boolean = "boolean"

    @property
    def is_multi(self) -> bool:
        return self == FieldType.select_many

    @property
    def is_select(self) -> bool:
        return self in (FieldType.select_one, FieldType.select_many)

    def validate_value(self, value: "FieldValue") -> None:
        match self:
            case FieldType.text:
                if value.value_text is None:
                    raise ValueError
            case FieldType.number:
                if value.value_number is None:
                    raise ValueError
            case FieldType.datetime:
                if value.value_date is None:
                    raise ValueError
            case FieldType.boolean:
                if value.value_boolean is None:
                    raise ValueError
            case FieldType.select_one | FieldType.select_many:
                if value.enum_id is None:
                    raise ValueError