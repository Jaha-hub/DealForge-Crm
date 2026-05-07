from src.backend.application.shared.errors import ApplicationError


class NotWebhookSourceError(ApplicationError):
    pass

class SourceNotFoundError(ApplicationError):
    pass
class CannotChangeSourceTypeError(ApplicationError):
    pass

class AssigmentPoolMemberNotFoundError(ApplicationError):
    pass
class AssigmentPoolMemberInactiveError(ApplicationError):
    pass
class AssigmentPoolInvalidRoleError(ApplicationError):
    pass

