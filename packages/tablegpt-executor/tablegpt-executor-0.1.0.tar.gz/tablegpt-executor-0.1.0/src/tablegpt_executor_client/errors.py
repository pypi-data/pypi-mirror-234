class ValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class OperatorValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class OperatorRuntimeError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class BadRequestError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class UnprocessableError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class RequestTimeoutError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class NotFoundError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class RateLimitExceededError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class UnknownError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def parse_error(status_code: int, payload: dict[str, str]) -> Exception:
    message = payload["detail"]
    if "error_type" in payload:
        error_type = payload["error_type"]
        match error_type:
            case "runtime":
                return OperatorRuntimeError(message)
            case "op_validation":
                return OperatorValidationError(message)

    match status_code:
        case 400:
            return BadRequestError(message)
        case 403:
            return UnprocessableError(message)
        case 424:
            return UnprocessableError(message)
        case 504:
            return RequestTimeoutError(message)
        case 404:
            return NotFoundError(message)
        case 429:
            return RateLimitExceededError(message)
        case _:
            # Fallback to an unknown error
            return UnknownError(message)
