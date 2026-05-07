from dataclasses import dataclass

from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.application.source.dtos.regenerate_webhook_secret import RegenerateWebhookSecretResult
from src.backend.application.source.errors import NotWebhookSourceError
from src.backend.domain.source.entity import Source
from src.backend.domain.source.enums.source_tupe.enum import SourceType
from src.backend.domain.user.entity import User


@dataclass
class RegenerateWebhookSecretUseCase:
    uow: UnitOfWork
    user: User
    source: Source

    async def execute(self):
        if self.source.source_type != SourceType.webhook:
            raise NotWebhookSourceError()
        token = self.source.regenerate_secret()
        async with self.uow:
            await self.uow.source.update(self.source)
            await self.uow.commit()
        return RegenerateWebhookSecretResult(
            secret_token=token
        )
