from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.backend.domain.funnel.value_objects.win_probability.value_object import WinProbability
from src.backend.domain.shared.entity import BaseEntity
from src.backend.domain.shared.mixins import TimeActionMixin
from src.backend.domain.shared.value_objects.hex.value_object import HexCode
from src.backend.domain.shared.value_objects.name.value_object import Name


@dataclass
class Funnel(BaseEntity,TimeActionMixin):
    name: Name
    is_deleted: bool = field(default=False)

    @classmethod
    def create(
            cls,
            name: str,
    ):
        return cls(
            name=Name(name),
        )

    def change_name(self, name: str):
        self.name = Name(name)
        self.touch()


    def delete(self):
        self.is_deleted = True
        self.touch()

@dataclass
class FunnelStage(BaseEntity, TimeActionMixin):
    funnel_id: UUID
    name: Name
    win_probability: WinProbability
    hex: HexCode = field(default_factory=HexCode("#6366F1"))
    order: int = field(default=0)

    @classmethod
    def create(
            cls,
            funnel_id: UUID,
            name: str,
            win_probability: int,
            hex: str,
            order: int,
    ):
        return cls(
            funnel_id=funnel_id,
            name=Name(name),
            win_probability=WinProbability(win_probability),
            hex=HexCode(hex),
            order=order,
        )

    def _touch(self)->None:
        self.updated_at = datetime.now()

    def change_order(self, order:int):
        self.order = order
        self.touch()

    def change(
            self,
            name:str,
            win_probability:int,
            hex:str,
    ):
        self.name = Name(name)
        self.win_probability = WinProbability(win_probability)
        self.hex = HexCode(hex)
        self.touch()

    def __hash__(self):
        return hash(self.id)

