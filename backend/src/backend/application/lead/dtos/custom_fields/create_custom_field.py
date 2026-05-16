from uuid import UUID

from pydantic import BaseModel

from src.backend.domain.lead.value_objects.field_type.value_object import FieldType


class CreateCustomFieldCommand(BaseModel):
    name: str
    type: FieldType
    enums_values: list[str]

class CreateCustomFieldResult(BaseModel):
    field_id: UUID