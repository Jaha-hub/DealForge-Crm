from src.backend.application.dtos.auth.login_user import LoginUserCommand, LoginUserResult
from src.backend.application.dtos.uow import UnitOfWork
from src.backend.application.services.security.hasher import Hasher
from src.backend.application.services.security.token import TokenService


class LoginUserUseCase:
    def __init__(
            self,
            uow: UnitOfWork,
            tokens: TokenService,
            hasher: Hasher
    ):
        self.uow = uow
        self.tokens = tokens
        self.hasher = hasher

    async def execute(
            self,
            cmd: LoginUserCommand,
    ):
        async with self.uow:
            user = await self.uow.users.get_by_username(cmd.username)

            if not user:
                raise

            if not self.hasher.verify(cmd.password, user.password_hash):
                raise

            if not user.ensure_active():
                raise

            access_token = self.tokens.encode({"sub": user.id})
            refresh_token = self.tokens.encode({"sub": user.id, "is_refresh": True})
            token_type = self.tokens.get_token_type()

            return LoginUserResult(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type=token_type,
            )