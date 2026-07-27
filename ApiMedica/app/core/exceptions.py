class AppException(Exception):
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code or "UNKNOWN_ERROR"
        super().__init__(self.detail)


class NotFoundException(AppException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail, error_code="NOT_FOUND")


class BadRequestException(AppException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=400, detail=detail, error_code="BAD_REQUEST")


class ExternalAPIException(AppException):
    def __init__(self, detail: str = "External API error"):
        super().__init__(status_code=502, detail=detail, error_code="EXTERNAL_API_ERROR")


class DatabaseException(AppException):
    def __init__(self, detail: str = "Database error"):
        super().__init__(status_code=500, detail=detail, error_code="DATABASE_ERROR")
