from uuid import UUID

from pydantic import BaseModel


class AssignLeadCommand(BaseModel):
    assign_to: UUID