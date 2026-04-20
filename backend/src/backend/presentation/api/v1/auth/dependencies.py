from fastapi.params import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.backend.application.auth.dtos.get_me import GetMeCommand
from src.backend.application.user.usecase.get_me import GetMeUseCase
from src.backend.domain.user.entity import User
from src.backend.infrastructure.db.sqlalchemy.core.uow import SqlalchemyUnitOfWork
from src.backend.infrastructure.security.agron2.hasher import Argon2Hasher
from src.backend.infrastructure.security.jose.token import JWTTokenService
from src.backend.presentation.api.v1.core.dependencies import get_uow
from tests.unit.domain.user.specifications.password import PasswordLengthSpecification, \
    PasswordUpperLetterSpecification, PasswordLowerLetterSpecification, PasswordDigitSpecification, \
    PasswordSpecialCharacterSpecification, PasswordDifferenceSpecification

schema = HTTPBearer()


# Authorization: Token

async def get_hasher() -> Argon2Hasher:
    return Argon2Hasher()


async def get_token_service() -> JWTTokenService:
    return JWTTokenService()


async def get_current_user(
        token: str = Depends(schema),
        tokens: JWTTokenService = Depends(get_token_service),
        uow: SqlalchemyUnitOfWork = Depends(get_uow),
) -> User:
    uc = GetMeUseCase(uow, tokens)
    user = await uc.execute(
        cmd=GetMeCommand(token=token),
    )
    return user


async def get_password_length_spec() -> PasswordLengthSpecification:
    return PasswordLengthSpecification()


async def get_password_upper_spec() -> PasswordUpperLetterSpecification:
    return PasswordUpperLetterSpecification()


async def get_password_lower_spec() -> PasswordLowerLetterSpecification:
    return PasswordLowerLetterSpecification()


async def get_password_digit_spec() -> PasswordDigitSpecification:
    return PasswordDigitSpecification()


async def get_password_special_spec() -> PasswordSpecialCharacterSpecification:
    return PasswordSpecialCharacterSpecification()


async def get_password_spec(
        length_spec: PasswordLengthSpecification = Depends(get_password_length_spec),
        upper_spec: PasswordUpperLetterSpecification = Depends(get_password_upper_spec),
        lower_spec: PasswordLowerLetterSpecification = Depends(get_password_lower_spec),
        digit_spec: PasswordDigitSpecification = Depends(get_password_digit_spec),
        special_spec: PasswordSpecialCharacterSpecification = Depends(get_password_special_spec),
):
    return length_spec & upper_spec & lower_spec & digit_spec & special_spec


async def get_password_diff_spec() -> PasswordDifferenceSpecification:
    return PasswordDifferenceSpecification()