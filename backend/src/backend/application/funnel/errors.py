from src.backend.domain.shared.errors import DomainError


class StageError(DomainError):
    pass

class StageNotFoundError(StageError):
    pass

class StageNotInFunnelError(StageError):
    pass

class FunnelNotFoundError(StageError):
    pass



