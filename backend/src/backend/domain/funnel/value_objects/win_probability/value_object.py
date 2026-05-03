from dataclasses import dataclass

from src.backend.domain.funnel.value_objects.win_probability.errors import InvalidProbabilityError


@dataclass(frozen=True)
class WinProbability:
    value: int

    def __post_init__(self):
        if not self.__validate():
            raise InvalidProbabilityError()
    def __validate(self)->bool:
        return 0 <= self.value <= 100