from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from starlette import status

from src.backend.application.auth.dtos.change_password import ChangePasswordCommand
from src.backend.application.auth.dtos.get_me import GetMeResult
from src.backend.application.auth.dtos.login_user import LoginUserCommand, LoginUserResult
from src.backend.application.auth.dtos.refresh_token import RefreshTokenCommand, RefreshTokenResult
from src.backend.application.auth.dtos.update_me import UpdateMeCommand
from src.backend.presentation.api.v1.auth.dependencies import UpdateMeDep, ChangePasswordDep, LoginDep, RefreshTokenDep, CurrentUserDep
from src.backend.presentation.api.v1.core.handlers.schemas import ExceptionSchema
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
            status.HTTP_401_UNAUTHORIZED: {
                "model": ExceptionSchema,
                "description": "Unauthorized Error"
        }
    }
)

@cbv(router)
class AuthRouter:

    @router.post(
        path="/login",
        name="Авторизация",
        status_code=status.HTTP_201_CREATED,
        response_model=LoginUserResult,
    )
    async def login(
        self,
        cmd: LoginUserCommand,
        uc: LoginDep,
    ):
        return await uc.execute(cmd)


    @router.post(
        path="/refresh",
        name="Обновление Токена",
        status_code=status.HTTP_201_CREATED,
        response_model=RefreshTokenResult,
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "model": ExceptionSchema,
            }
        }
    )
    async def refresh(
        self,
        cmd: RefreshTokenCommand,
        uc: RefreshTokenDep,
    ):
        return await uc.execute(cmd)


    @router.get(
        "/me",
        name="Получение Персональной Информации",
        status_code=status.HTTP_200_OK,
        response_model=GetMeResult
    )
    async def get_me(
        self,
        user: CurrentUserDep,
    ):
        return GetMeResult(
            id=user.id,
            first_name=user.first_name.value,
            last_name=user.last_name.value,
            email=user.email.value,
            username=user.username.value,
            last_interaction=user.last_interaction,
            is_active=user.is_active,
            role=user.role
        )


    @router.post(
        path="/change-password",
        name="Изменение Пароля",
        status_code=status.HTTP_204_NO_CONTENT,
        responses={
            status.HTTP_400_BAD_REQUEST: {
                "model": ExceptionSchema,
                "description": "Bad Request Error"
            }
        }
    )
    async def change_password(
        self,
        cmd: ChangePasswordCommand,
        uc: ChangePasswordDep,
    ):
        await uc.execute(cmd)


    @router.patch(
        path="/me",
        name="Обновление Персональной Информации",
        status_code=status.HTTP_204_NO_CONTENT,
        responses={
            status.HTTP_409_CONFLICT: {
                "model": ExceptionSchema,
                "description": "Conflict Error"
            }
        }
    )
    async def update_me(
        self,
        cmd: UpdateMeCommand,
        uc: UpdateMeDep,
    ):
        await uc.execute(cmd)