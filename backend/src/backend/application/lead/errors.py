from src.backend.application.shared.errors import ApplicationError


class CustomFieldError(ApplicationError):
    pass

class SlugAlreadyExistsError(ApplicationError):
    pass

class CustomFieldNameAlreadyExistsError(ApplicationError):
    pass
class SelectFieldWithoutEnumsError(ApplicationError):
    pass
class EnumsNotAllowForNonSelectError(ApplicationError):
    pass

class CustomFieldNotFoundError(ApplicationError):
    pass

class EnumInUseError(ApplicationError):
    pass

