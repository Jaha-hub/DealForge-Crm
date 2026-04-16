from fastapi.params import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.backend.application.auth.dtos.get_me import GetMeCommand
from src.backend.application.user.usecase.get_me import GetMeUseCase
from src.backend.domain.user.entity import User
from src.backend.infrastructure.db.sqlalchemy.core.uow import SqlalchemyUnitOfWork
from src.backend.infrastructure.security.agron2.hasher import Argon2Hasher
from src.backend.infrastructure.security.jose.token import JWTTokenService
from src.backend.presentation.api.v1.core.dependencies import get_uow

scheme = HTTPBearer()
async def get_hasher() -> Argon2Hasher:
    return Argon2Hasher()


async def get_token_service() -> JWTTokenService:
    return JWTTokenService()

async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(scheme),
    tokens: JWTTokenService = Depends(get_token_service),
    uow: SqlalchemyUnitOfWork = Depends(get_uow),
) -> User:
    uc = GetMeUseCase(uow, tokens)
    user = await uc.execute(
        cmd=GetMeCommand(token=token.credentials),
    )
    return user
