from enum import StrEnum


class AssignmentStrategy(StrEnum):
    manual = "manual"
    round_robin = "round_robin"
    leats_loaded = "leats_loaded"