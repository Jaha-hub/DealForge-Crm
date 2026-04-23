from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status

from src.backend.application.funnel.dtos.create_funnel_stage import CreateFunnelStageResult, CreateFunnelStageCommand
from src.backend.application.funnel.services.stage_ordering import FunnelStageOrderingService
from src.backend.application.funnel.use_cases.create_funnel_stage import CreateFunnelStageUseCase
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.funnel.entity import Funnel
from src.backend.domain.user.entity import User
from src.backend.presentation.api.v1.auth.dependencies import get_current_user
from src.backend.presentation.api.v1.core.dependencies import get_uow
from src.backend.presentation.api.v1.funnel.dependencies import get_funnel, get_ordering

router = APIRouter(
    prefix="/{funnel_id}/stages",
)


@cbv(router)
class FunnelStageRouter:
    uow: UnitOfWork = Depends(get_uow)
    user: User = Depends(get_current_user)
    funnel: Funnel = Depends(get_funnel)

    async def create_funnel_stage(
            self,
            request: CreateFunnelStageCommand,
            ordering: FunnelStageOrderingService = Depends(get_ordering),
    ):
        uc = CreateFunnelStageUseCase(
            uow=self.uow,
            funnel=self.funnel,
            user=self.user,
            ordering=ordering,
        )
        response = await uc.execute(cmd=request)
        return response

    