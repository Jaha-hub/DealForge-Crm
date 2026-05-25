from uuid import UUID

from pydantic import BaseModel


class CreateLeadCommand(BaseModel):
    name: str
    fullname: str
    email: str | None = None
    phone: str | None = None
    telegram: str | None = None
    assigned_to: UUID
    funnel_id: UUID


class CustomFieldValueOut(BaseModel):
    field_id: UUID
    field_name: str
    field_type: str
    value_id: UUID
    value: str | None


class CreateLeadResult(BaseModel):
    lead_id: UUID
    duplicate_warning: bool = False
    duplicated_lead_ids: list[UUID] = []