from uuid import UUID

from sqlalchemy import select

from src.backend.application.funnel.repository import FunnelStageRepository
from src.backend.domain.funnel.entity import FunnelStage
from src.backend.domain.funnel.value_objects.win_probability.value_object import WinProbability
from src.backend.domain.shared.value_objects.hex.value_object import HexCode
from src.backend.domain.shared.value_objects.name.value_object import Name
from src.backend.infrastructure.db.sqlalchemy.core.repository.repository import SqlalchemyRepository
from src.backend.infrastructure.db.sqlalchemy.funnel.models import FunnelStageModel


def to_model(stage: FunnelStage)-> FunnelStageModel:
    return FunnelStageModel(
        id=stage.id,
        funnel_id=stage.funnel_id,
        name=str(stage.name),
        win_probability=int(stage.win_probability),
        hex=str(stage.hex),
        order=stage.order,
        created_at=stage.created_at,
        updated_at=stage.updated_at,
    )

def to_entity(stage: FunnelStageModel)-> FunnelStage:
    return FunnelStage(
        id=stage.id,
        funnel_id=stage.funnel_id,
        name=Name(stage.name),
        win_probability=WinProbability(stage.win_probability),
        hex=HexCode(stage.hex),
        order=stage.order,
        created_at=stage.created_at,
        updated_at=stage.updated_at,
    )

class SqlalchemyFunnelStageRepository(SqlalchemyRepository,FunnelStageRepository):

    async def get_funnel_stage_by_id(self, stage_id: UUID) -> FunnelStage | None:
        stmt = select(FunnelStageModel).where(FunnelStageModel.id == stage_id)
        result = await self.session.execute(stmt)
        stage = result.scalar_one_or_none()
        return to_entity(stage) if stage else None

    async def update_funnel_stage(self, stage: FunnelStage) -> FunnelStage:
        instance = to_model(stage)
        self.session.add(instance)
        await self.session.flush()
        return to_entity(instance)

    async def delete_funnel_stage(self, stage: FunnelStage) -> None:
        instance = to_model(stage)
        await self.session.delete(instance)
        await self.session.flush()

    async def save_all(self, stages: list[FunnelStage]) -> None:
        for s in stages:
            instance = to_model(s)
            await self.session.merge(instance)
        await self.session.flush()

    async def get_funnel_stages(self, funnel_id: UUID) -> list[FunnelStage] | None:
        stmt = select(FunnelStageModel).where(FunnelStageModel.funnel_id == funnel_id)
        result = await self.session.execute(stmt)
        stages = result.scalars().all()
        return [to_entity(s) for s in stages]