from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status

from src.backend.application.user.dtos.create_user import CreateUserCommand
from src.backend.application.user.usecase.create_user import CreateUserUseCase
from src.backend.domain.user.entity import User
from src.backend.infrastructure.db.sqlalchemy.core.uow import SqlalchemyUnitOfWork
from src.backend.infrastructure.security.agron2.hasher import Argon2Hasher
from src.backend.presentation.api.v1.auth.dependencies import get_current_user, get_hasher, get_password_spec
from src.backend.presentation.api.v1.core.dependencies import get_uow
from tests.unit.domain.shared.specification import Specification


router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@cbv(router)
class UserRouter:
    uow: SqlalchemyUnitOfWork = Depends(get_uow)
    user: User = Depends(get_current_user)

    @router.post(
        "/",
        name="Создания Пользователя",
        status_code=status.HTTP_201_CREATED,
    )
    async def create_user(
            self,
            request: CreateUserCommand,
            hasher: Argon2Hasher = Depends(get_hasher),
            password_spec: Specification[str] = Depends(get_password_spec)
    ):
        uc = CreateUserUseCase(
            uow=self.uow,
            actor=self.user,
            hasher=hasher,
            password_spec=password_spec,
        )

        response = await uc.execute(
            cmd=request
        )
        return response