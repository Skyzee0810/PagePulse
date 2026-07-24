class AuditServiceError(Exception):
    """Base exception for audit service errors."""


class AuditTimeoutError(AuditServiceError):
    """Raised when the target URL times out."""


class AuditConnectionError(AuditServiceError):
    """Raised when the target URL cannot be reached."""