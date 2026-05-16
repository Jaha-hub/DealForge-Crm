from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status

from src.backend.application.funnel.dtos.create_funnel import CreateFunnelResult, CreateFunnelCommand
from src.backend.application.funnel.dtos.list_funnel import ListFunnelCommand
from src.backend.application.funnel.dtos.update_funnel import UpdateFunnelCommand
from src.backend.application.funnel.use_cases.create_funnel import CreateFunnelUseCase
from src.backend.application.funnel.use_cases.delete_funnel import DeleteFunnelUseCase
from src.backend.application.funnel.use_cases.list_funnel import ListFunnelUseCase
from src.backend.application.funnel.use_cases.update_funnel import UpdateFunnelUseCase
from src.backend.application.shared.dtos.pagination import PageResult
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

    @router.put(
        "/funnel_update/{funnel_id}",
        response_model=Funnel
    )
    async def update_funnel(
            self,
            request: UpdateFunnelCommand,
            funnel: Funnel = Depends(get_funnel),
    ):
        uc = UpdateFunnelUseCase(
            uow=self.uow,
            user=self.user,
            funnel=funnel,
        )
        response = await uc.execute(request)
        return response

    async def delete_funnel(
            self,
            funnel: Funnel = Depends(get_funnel),
    ):
        uc = DeleteFunnelUseCase(
            uow=self.uow,
            user=self.user,
            funnel=funnel,
        )
        await uc.execute()
        return None

    @router.get(
        "/funnels",
        response_model=PageResult[Funnel]
    )
    async def list_funnels(
            self,
            command: ListFunnelCommand = Depends(),
    ):
        uc = ListFunnelUseCase(
            uow=self.uow,
            user=self.user,
        )
        result = await uc.execute(command)
        return result