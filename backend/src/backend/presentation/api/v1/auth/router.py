from fastapi import Depends, APIRouter
from fastapi_utils.cbv import cbv
from starlette import status

from src.backend.application.auth.dtos.login_user import LoginUserCommand
from src.backend.application.auth.use_cases.login_user import LoginUserUseCase
from src.backend.infrastructure.db.sqlalchemy.core.uow import SqlalchemyUnitOfWork
from src.backend.presentation.api.v1.auth.dependencies import get_hasher, get_token_service
from src.backend.infrastructure.security.agron2.hasher import Argon2Hasher
from src.backend.infrastructure.security.jose.token import JWTTokenService
from src.backend.presentation.api.v1.core.dependencies import get_uow
router = APIRouter()

@cbv(router)
class AuthRouter:
    uow: SqlalchemyUnitOfWork = Depends(get_uow)

    @router.post(
        path="/login",
        name="Авторизация",
        status_code=status.HTTP_201_CREATED
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