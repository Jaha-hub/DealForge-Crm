from uuid import UUID
from pydantic import BaseModel

class DeleteUserCommand(BaseModel):
    user_id: UUID

class DeleteUserResult(BaseModel):
    user_id: UUID