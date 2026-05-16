from uuid import UUID
from pydantic import BaseModel
from src.backend.domain.user.entity import UserRole


class GetMeCommand(BaseModel):
    user_id: UUID


class GetMeResult(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    username: str
    email: str
    role: UserRole