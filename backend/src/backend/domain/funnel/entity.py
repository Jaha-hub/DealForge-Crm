from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.backend.domain.funnel.value_objects.win_probability.value_object import WinProbability
from src.backend.domain.shared.value_objects.hex.value_object import HexCode
from src.backend.domain.shared.value_objects.name.value_object import Name


@dataclass
class Funnel:
    id: UUID
    name: Name
    is_deleted: bool = field(default=False)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def create(
            cls,
            id: UUID,
            name: str,
    ):
        return cls(
            id=id,
            name=Name(name),
        )

    def _touch(self) -> None:
        self.updated_at = datetime.now()

    def change_name(self, name: str):
        self.name = Name(name)
        self._touch()


    def delete(self):
        self.is_deleted = True

@dataclass
class FunnelStage:
    id: UUID
    funnel_id: UUID
    name: Name
    win_probability: WinProbability
    hex: HexCode = field(default_factory=HexCode("#6366F1"))
    order: int = field(default=0)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    @classmethod
    def create(
            cls,
            id: UUID,
            funnel_id: UUID,
            name: str,
            win_probability: int,
            hex: str,
            order: int,
    ):
        return cls(
            id=id,
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
        self._touch()

    def change(
            self,
            name:str,
            win_probability:int,
            hex:str,
    ):
        self.name = Name(name)
        self.win_probability = WinProbability(win_probability)
        self.hex = HexCode(hex)
        self._touch()

    def __hash__(self):
        return hash(self.id)

