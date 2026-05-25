from uuid import UUID

from pydantic import BaseModel


class MoveLeadCommand(BaseModel):
    stage_id: UUID