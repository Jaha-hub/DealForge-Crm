from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GetLeadCommand(BaseModel):
    lead_id: UUID


class GetLeadResult(BaseModel):
    id: UUID
    name: str
    fullname: str
    email: str | None = None
    phone: str | None = None
    telegram: str | None = None
    funnel_id: UUID | None
    stage_id: UUID
    source_id: UUID
    assigned_to: UUID | None
    is_deleted: bool
    custom_values: list
    created_at: datetime
    updated_at: datetime