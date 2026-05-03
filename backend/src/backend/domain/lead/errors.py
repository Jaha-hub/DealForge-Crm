from src.backend.domain.shared.errors import DomainError


class FieldTypeNotSelectError(DomainError):
    pass

class EnumValueAlreadyExistsError(DomainError):
    pass

class InvalidEnumIdError(DomainError):
    pass