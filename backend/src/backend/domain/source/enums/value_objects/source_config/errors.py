from src.backend.domain.shared.errors import DomainError


class EmptyWebhookSecretError(DomainError):
    pass

class InvalidFieldMappingError(DomainError):
    pass

class CustomFieldKindRequiresFieldIdError(DomainError):
    pass

class FieldIdNotAllowedForKindError(DomainError):
    pass
class InvalidSlugError(DomainError):
    pass

class EmptyFormFieldError(DomainError):
    pass

class DuplicateFormFieldError(DomainError):
    pass

class NotWebhookSourceError(DomainError):
    pass

