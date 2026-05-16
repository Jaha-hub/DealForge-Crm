from dataclasses import dataclass
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class GetCustomFieldCommand(BaseModel):
    field_id: UUID
    include_deleted: bool

@dataclass
class CustomFieldResult:
    id: UUID
    name: str
    type: str
    enum_values: Optional[List[str]]