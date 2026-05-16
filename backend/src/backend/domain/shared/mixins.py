import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID

@dataclass(kw_only=True)
class IDMixin:
    """
    Mixin для уникальных идентификаторов Сущностей

    Attributes:
        id: Уникальный идентификатор
    """

    id: UUID = field(default_factory=uuid.uuid4)


@dataclass(kw_only=True)
class TimeActionMixin:
    """
    Mixin для временных меток используется как дополнение для основной сущности

    Attributes:
        created_at: Временная метка создания сущности
        updated_at: Временная метка обновления сущности
    """

    created_at: datetime = field(default_factory=lambda :
    datetime.now(tz=timezone.utc))
    updated_at: datetime = field(default_factory=lambda :datetime.now(tz=timezone.utc))

    def touch(self) -> None:
        """
        Будет фиксировать время изменения
        :return:
        """
        self.updated_at = datetime.now(tz=timezone.utc)