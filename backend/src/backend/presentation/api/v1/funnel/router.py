from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status

from src.backend.application.funnel.dtos.create_funnel import CreateFunnelResult, CreateFunnelCommand
from src.backend.application.funnel.use_cases.create_funnel import CreateFunnelUseCase
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.funnel.entity import Funnel
from src.backend.domain.user.entity import User
from src.backend.presentation.api.v1.auth.dependencies import get_current_user
from src.backend.presentation.api.v1.core.dependencies import get_uow
from src.backend.presentation.api.v1.funnel.dependencies import get_funnel

router = APIRouter(
    prefix="/funnels",
    tags=["funnels"]
)

@cbv(router)
class FunnelRouter:
    uow: UnitOfWork = Depends(get_uow)
    user: User = Depends(get_current_user)

    @router.post(
        "/",
        status_code=status.HTTP_201_CREATED,
        response_model=CreateFunnelResult,
    )
    async def create_funnel(
            self,
            request: CreateFunnelCommand
    ):
        uc = CreateFunnelUseCase(
            uow=self.uow,
            user=self.user,
        )
        response = await uc.execute(request)
        return response

    @router.get(
        "/{funnel_id}",
        response_model=Funnel
    )
    async def get_funnel(
            self,
            funnel: Funnel = Depends(get_funnel)
    ):
        return funnel