from fastapi import Depends, APIRouter
from fastapi_utils.cbv import cbv
from starlette import status

from src.backend.application.auth.dtos.change_password import ChangePasswordCommand
from src.backend.application.auth.dtos.get_me import GetMeResult
from src.backend.application.auth.dtos.login_user import LoginUserCommand, LoginUserResult
from src.backend.application.auth.dtos.refresh_token import RefreshTokenCommand, RefreshTokenResult
from src.backend.application.auth.dtos.update_me import UpdateMeCommand
from src.backend.application.auth.use_cases.change_password import ChangePasswordUseCase
from src.backend.application.auth.use_cases.login_user import LoginUserUseCase
from src.backend.application.auth.use_cases.refresh_token import RefreshTokenUseCase
from src.backend.application.auth.use_cases.update_me import UpdateMeUseCase
from src.backend.domain.user.entity import User
from src.backend.infrastructure.db.sqlalchemy.core.uow import SqlalchemyUnitOfWork
from src.backend.presentation.api.v1.auth.dependencies import get_hasher, get_token_service, get_current_user, \
    get_password_spec, get_password_diff_spec
from src.backend.infrastructure.security.agron2.hasher import Argon2Hasher
from src.backend.infrastructure.security.jose.token import JWTTokenService
from src.backend.presentation.api.v1.core.dependencies import get_uow
from src.backend.presentation.api.v1.core.handlers.schemas import ExceptionSchema
from tests.unit.domain.shared.specification import Specification
from tests.unit.domain.user.specifications.password import PasswordDifferenceSpecification

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
    uow: SqlalchemyUnitOfWork = Depends(get_uow)

    @router.post(
        path="/login",
        name="Авторизация",
        status_code=status.HTTP_201_CREATED,
        response_model=LoginUserResult,

    )
    async def login(
        self,
        request: LoginUserCommand,
        hasher: Argon2Hasher = Depends(get_hasher),
        tokens: JWTTokenService = Depends(get_token_service)
    ):
        uc = LoginUserUseCase(
            uow=self.uow,
            tokens=tokens,
            hasher=hasher,
        )
        response = await uc.execute(
            cmd=request,
        )

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
            request: RefreshTokenCommand,
            tokens: JWTTokenService = Depends(get_token_service)
    ):
        uc = RefreshTokenUseCase(
            uow=self.uow,
            tokens=tokens,
        )
        response = await uc.execute(
            cmd=request
        )
        return response
    @router.get(
        "/me",
        name="Получение Персональной Информации",
        status_code=status.HTTP_200_OK,
        response_model=GetMeResult
    )
    async def get_me(
            self,
            user: User = Depends(get_current_user)
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
            request: ChangePasswordCommand,
            user: User = Depends(get_current_user),
            hasher: Argon2Hasher = Depends(get_hasher),
            password_spec: Specification[str] = Depends(get_password_spec),
            password_diff_spec: PasswordDifferenceSpecification = Depends(get_password_diff_spec)
    ):
        uc = ChangePasswordUseCase(
            uow=self.uow,
            hasher=hasher,
            password_spec=password_spec,
            password_diff_spec=password_diff_spec,
            user=user,
        )
        await uc.execute(
            cmd=request
        )

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
                request: UpdateMeCommand,
                user: User = Depends(get_current_user),
        ):
            uc = UpdateMeUseCase(
                uow=self.uow,
                user=user,
            )
            await uc.execute(
                cmd=request
            )