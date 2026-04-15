from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from src.backend.domain.user.entity import UserRole


class UpdateUserCommand(BaseModel):
    user_id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UpdateUserResult(BaseModel):
    user_id: UUID