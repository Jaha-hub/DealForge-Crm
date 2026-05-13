from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.backend.domain.lead.value_objects.field_type.value_object import FieldType


class CustomFieldEnumViewDTO(BaseModel):
    id: UUID
    value: str

class CustomFieldViewDTO(BaseModel):
    id: UUID
    name: str
    field_type: FieldType
    enums: list[CustomFieldEnumViewDTO]
    is_deleted: bool
    created_at: datetime
    updated_at: datetime