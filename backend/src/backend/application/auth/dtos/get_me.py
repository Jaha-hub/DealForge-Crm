from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

class GetMeCommand(BaseModel):
    token: str

class GetMeResult(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    username: str
    email: str
    last_interaction: datetime
    is_active: bool