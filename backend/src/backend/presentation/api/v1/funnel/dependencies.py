from uuid import UUID

from fastapi.params import Depends

from src.backend.application.funnel.dtos.get_funnel import GetFunnelCommand
from src.backend.application.funnel.dtos.get_funnel_stage import GetFunnelStageCommand
from src.backend.application.funnel.services.stage_ordering import FunnelStageOrderingService
from src.backend.application.funnel.use_cases.get_funnel import GetFunnelUseCase
from src.backend.application.funnel.use_cases.get_funnel_stage import GetFunnelStageUseCase
from src.backend.domain.funnel.entity import Funnel
from src.backend.domain.user.entity import User
from src.backend.infrastructure.db.sqlalchemy.core.uow import SqlalchemyUnitOfWork
from src.backend.presentation.api.v1.auth.dependencies import get_current_user
from src.backend.presentation.api.v1.core.dependencies import get_uow


async def get_funnel(
        funnel_id:UUID,
        user : User = Depends(get_current_user),
        uow: SqlalchemyUnitOfWork = Depends(get_uow),
):
    uc = GetFunnelUseCase(
        uow=uow,
        user=user,
    )
    funnel = await uc.execute(GetFunnelCommand(funnel_id=funnel_id))
    return funnel

async def get_stage(
        stage_id:UUID,
        funnel: Funnel = Depends(get_funnel),
        uow: SqlalchemyUnitOfWork = Depends(get_uow),
):
    uc = GetFunnelStageUseCase(
        uow=uow,
        funnel=funnel,
    )
    stage = await uc.execute(GetFunnelStageCommand(stage_id=stage_id))
    return stage

def get_ordering()-> FunnelStageOrderingService:
    return FunnelStageOrderingService()