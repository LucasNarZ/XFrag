class DomainError(Exception):
    status_code = 400
    code = "DOMAIN_ERROR"

    def __init__(self, message: str, details: list[dict] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details


class AuthenticationError(DomainError):
    status_code = 401
    code = "AUTHENTICATION_ERROR"


class ConflictError(DomainError):
    status_code = 409
    code = "CONFLICT_ERROR"


class NotFoundError(DomainError):
    status_code = 404
    code = "NOT_FOUND"


class ValidationError(DomainError):
    status_code = 422
    code = "VALIDATION_ERROR"
