from src.backend.application.shared.errors import ApplicationError


class CustomFieldError(ApplicationError):
    pass

class SlugAlreadyExistsError(ApplicationError):
    pass
