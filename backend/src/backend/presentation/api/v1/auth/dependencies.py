from typing import Annotated
from fastapi import Depends

from fastapi.security import HTTPBearer
from src.backend.application.auth.dtos.get_me import GetMeCommand
from src.backend.application.auth.use_cases.change_password import ChangePasswordUseCase
from src.backend.application.auth.use_cases.login_user import LoginUserUseCase
from src.backend.application.auth.use_cases.refresh_token import RefreshTokenUseCase
from src.backend.application.auth.use_cases.update_me import UpdateMeUseCase
from src.backend.application.user.usecase.get_me import GetMeUseCase
from src.backend.domain.user.entity import User
from src.backend.infrastructure.security.agron2.hasher import Argon2Hasher
from src.backend.infrastructure.security.jose.token import JWTTokenService
from src.backend.presentation.api.v1.core.dependencies import get_uow, UoWDep
from tests.unit.domain.shared.specification import Specification
from tests.unit.domain.user.specifications.password import PasswordLengthSpecification, \
    PasswordUpperLetterSpecification, PasswordLowerLetterSpecification, PasswordDigitSpecification, \
    PasswordSpecialCharacterSpecification, PasswordDifferenceSpecification

schema = HTTPBearer()


# Authorization: Token



async def get_hasher() -> Argon2Hasher:
    return Argon2Hasher()


HasherDep = Annotated[
    Argon2Hasher,
    Depends(get_hasher),
]


async def get_token_service() -> JWTTokenService:
    return JWTTokenService()


TokenServiceDep = Annotated[
    JWTTokenService,
    Depends(get_token_service),
]
UoWDep

async def get_current_user(
    tokens: TokenServiceDep,
    uow: UoWDep,
    token: str = Depends(schema),
) -> User:
    uc = GetMeUseCase(
        uow=uow,
        tokens=tokens,
    )
    return await uc.execute(
        cmd=GetMeCommand(token=token),
    )


CurrentUserDep = Annotated[
    User,
    Depends(get_current_user),
]


async def get_password_length_spec() -> PasswordLengthSpecification:
    return PasswordLengthSpecification()


LengthSpecDep = Annotated[
    PasswordLengthSpecification,
    Depends(get_password_length_spec),
]


async def get_password_upper_spec() -> PasswordUpperLetterSpecification:
    return PasswordUpperLetterSpecification()


UpperSpecDep = Annotated[
    PasswordUpperLetterSpecification,
    Depends(get_password_upper_spec),
]


async def get_password_lower_spec() -> PasswordLowerLetterSpecification:
    return PasswordLowerLetterSpecification()


LowerSpecDep = Annotated[
    PasswordLowerLetterSpecification,
    Depends(get_password_lower_spec),
]


async def get_password_digit_spec() -> PasswordDigitSpecification:
    return PasswordDigitSpecification()


DigitSpecDep = Annotated[
    PasswordDigitSpecification,
    Depends(get_password_digit_spec),
]


async def get_password_special_spec() -> PasswordSpecialCharacterSpecification:
    return PasswordSpecialCharacterSpecification()


SpecialSpecDep = Annotated[
    PasswordSpecialCharacterSpecification,
    Depends(get_password_special_spec),
]


async def get_password_spec(
    length: LengthSpecDep,
    upper: UpperSpecDep,
    lower: LowerSpecDep,
    digit: DigitSpecDep,
    special: SpecialSpecDep,
) -> Specification:
    return length & upper & lower & digit & special


PasswordSpecDep = Annotated[
    Specification,
    Depends(get_password_spec),
]


async def get_password_diff_spec() -> PasswordDifferenceSpecification:
    return PasswordDifferenceSpecification()


PasswordDiffSpecDep = Annotated[
    PasswordDifferenceSpecification,
    Depends(get_password_diff_spec),
]


def get_login_use_case(
    uow: UoWDep,
    hasher: HasherDep,
    tokens: TokenServiceDep,
) -> LoginUserUseCase:
    return LoginUserUseCase(
        uow=uow,
        hasher=hasher,
        tokens=tokens,
    )


LoginDep = Annotated[
    LoginUserUseCase,
    Depends(get_login_use_case),
]


def get_me_use_case(
    uow: UoWDep,
    tokens: TokenServiceDep,
) -> GetMeUseCase:
    return GetMeUseCase(
        uow=uow,
        tokens=tokens,
    )


GetMeDep = Annotated[
    GetMeUseCase,
    Depends(get_me_use_case),
]


def get_refresh_token_use_case(
    uow: UoWDep,
    tokens: TokenServiceDep,
) -> RefreshTokenUseCase:
    return RefreshTokenUseCase(
        uow=uow,
        tokens=tokens,
    )


RefreshTokenDep = Annotated[
    RefreshTokenUseCase,
    Depends(get_refresh_token_use_case),
]


def get_change_password_use_case(
    uow: UoWDep,
    user: CurrentUserDep,
    hasher: HasherDep,
    password_spec: PasswordSpecDep,
    password_diff_spec: PasswordDiffSpecDep,
) -> ChangePasswordUseCase:
    return ChangePasswordUseCase(
        uow=uow,
        user=user,
        hasher=hasher,
        password_spec=password_spec,
        password_diff_spec=password_diff_spec,
    )


ChangePasswordDep = Annotated[
    ChangePasswordUseCase,
    Depends(get_change_password_use_case),
]


def get_update_me_use_case(
    uow: UoWDep,
    user: CurrentUserDep,
) -> UpdateMeUseCase:
    return UpdateMeUseCase(
        uow=uow,
        user=user,
    )


UpdateMeDep = Annotated[
    UpdateMeUseCase,
    Depends(get_update_me_use_case),
]