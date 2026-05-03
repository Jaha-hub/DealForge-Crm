from dataclasses import dataclass
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class GetCustomFieldCommand(BaseModel):
    id: UUID

@dataclass
class CustomFieldResult:
    id: UUID
    name: str
    type: str
    enum_values: Optional[List[str]]