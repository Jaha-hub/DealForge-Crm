from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status
from src.backend.application.funnel.dtos.create_funnel_stage import CreateFunnelStageCommand
from src.backend.application.funnel.dtos.create_funnel_stage import CreateFunnelStageResult
from src.backend.application.funnel.dtos.update_funnel_stage import UpdateFunnelStageCommand
from src.backend.application.funnel.services.stage_ordering import FunnelStageOrderingService
from src.backend.application.funnel.use_cases.create_funnel_stage import CreateFunnelStageUseCase
from src.backend.application.funnel.use_cases.delete_funnel_stage import DeleteFunnelStageUseCase
from src.backend.application.funnel.use_cases.list_funnel_stage import ListFunnelStageUseCase
from src.backend.application.funnel.use_cases.update_funnel_stage import UpdateFunnelStageUseCase
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.funnel.entity import Funnel, FunnelStage
from src.backend.domain.user.entity import User
from src.backend.presentation.api.v1.auth.dependencies import get_current_user
from src.backend.presentation.api.v1.core.dependencies import get_uow
from src.backend.presentation.api.v1.funnel.dependencies import get_funnel, get_ordering, get_stage

router = APIRouter(
    prefix="/{funnel_id}/stages",
)


@cbv(router)
class FunnelStageRouter:
    uow: UnitOfWork = Depends(get_uow)
    user: User = Depends(get_current_user)
    funnel: Funnel = Depends(get_funnel)
    @router.post(
        "/",
        response_model=CreateFunnelStageResult,
        status_code=status.HTTP_201_CREATED,
    )
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
    @router.put(
        "/{stage_id}",
        status_code=status.HTTP_200_OK
    )
    async def update_funnel_stage(
            self,
            request: UpdateFunnelStageCommand,
            stage: FunnelStage = Depends(get_stage),
    ):
        uc = UpdateFunnelStageUseCase(
            uow=self.uow,
            funnel=self.funnel,
            stage=stage,
            user=self.user
        )
        await uc.execute(cmd=request)
    @router.delete(
        "/{stage_id}",
        status_code=status.HTTP_404_NOT_FOUND
    )
    async def delete_funnel_stage(
            self,
            stage: FunnelStage = Depends(get_stage),
            ordering: FunnelStageOrderingService = Depends(get_ordering),
    ):
        uc = DeleteFunnelStageUseCase(
            uow=self.uow,
            funnel=self.funnel,
            stage=stage,
            user=self.user,
            ordering=ordering,
        )
        await uc.execute()
    @router.get(
        "/{stage_id}",
        status_code=status.HTTP_200_OK,
    )
    async def get_funnel_stage(
            self,
            stage: FunnelStage = Depends(get_stage),
    ):
        return stage
    @router.get(
        "/",
        status_code=status.HTTP_200_OK,
    )
    async def list_funnel_stages(
            self,
            ordering: FunnelStageOrderingService = Depends(get_ordering),
    ):
        uc = ListFunnelStageUseCase(
            uow=self.uow,
            funnel=self.funnel,
            ordering=ordering,
        )
        return await uc.execute()