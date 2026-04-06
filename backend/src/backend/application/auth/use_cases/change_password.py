from src.backend.application.auth.dtos.change_password import ChangePasswordCommand
from src.backend.application.auth.errors import AuthUserNotFoundError, InvalidPasswordError
from src.backend.application.auth.interfaces.security.hasher import Hasher
from src.backend.application.shared.interfaces.uow import UnitOfWork


class ChangePasswordUseCase:

    def __init__(
        self,
        uow: UnitOfWork,
        hasher: Hasher,
    ):
        self.uow = uow
        self.hasher = hasher

    async def execute(self, cmd: ChangePasswordCommand):
        async with self.uow as uow:
            user = await uow.find_by_id(cmd.user_id)

            if not user:
                raise AuthUserNotFoundError()

            if not self.hasher.verify(cmd.old_password, user.password_hash):
                raise InvalidPasswordError()

            user.password_hash = self.hasher.hash(cmd.new_password)

            await self.uow.users.update(user)
            await uow.commit()