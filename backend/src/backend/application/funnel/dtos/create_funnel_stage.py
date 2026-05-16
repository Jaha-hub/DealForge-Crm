from pydantic import BaseModel

from src.backend.domain.funnel.entity import Funnel


class CreateFunnelStageCommand(BaseModel):
    name: str
    win_probability: int
    hex: str
    position: int | None = None

class CreateFunnelStageResult(BaseModel):
    stage_id: int