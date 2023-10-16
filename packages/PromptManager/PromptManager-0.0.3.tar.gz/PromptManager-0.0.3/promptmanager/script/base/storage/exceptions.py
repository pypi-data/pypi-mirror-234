from promptmanager.script.base.schema import PMException


class InvalidKeyException(PMException):
    """Raised when a key is invalid; e.g., uses incorrect characters."""
