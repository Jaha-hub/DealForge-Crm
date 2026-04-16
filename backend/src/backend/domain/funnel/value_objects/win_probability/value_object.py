from dataclasses import dataclass

@dataclass(frozen=True)
class WinProbability:
    value: int

    def __post_init__(self):
        if not self.__validate():
            raise
    def __validate(self)->bool:
        return 0 <= self.value <= 100