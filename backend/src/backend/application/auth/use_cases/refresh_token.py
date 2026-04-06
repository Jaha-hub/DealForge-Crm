from src.backend.application.auth.dtos.change_password import ChangePasswordCommand
from src.backend.application.auth.interfaces.security.hasher import Hasher
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.user.entity import User


class ChangePasswordUseCase:
    def __init__(
            self,
            uow: UnitOfWork,
            hasher: Hasher,

    ):
        self._uow = uow
        self._hasher = hasher

    async def execute(self, cmd: ChangePasswordCommand):
        async with self._uow as uow:
            user = await uow.find_by_id(cmd.user_id)

            if not user:
                pass

            if not self._hasher.verify(cmd.old_password, user.password_hash):
                raise
