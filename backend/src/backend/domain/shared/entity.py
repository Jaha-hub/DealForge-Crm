from dataclasses import dataclass

from src.backend.infrastructure.db.sqlalchemy.core.mixins import UUIDMixin





@dataclass
class BaseEntity(UUIDMixin):
    """
    Базовая Сущность
    """

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other: "BaseEntity"):
        return self.id == other.id