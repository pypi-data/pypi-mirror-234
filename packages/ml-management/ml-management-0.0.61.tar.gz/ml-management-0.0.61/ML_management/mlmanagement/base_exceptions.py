"""Base classes for custom exceptions used in project."""


class MLMBaseException(Exception):
    """Base exception for all custom exceptions."""

    pass


class ServerException(MLMBaseException):
    """Base exception for all server mlmanager exceptions."""

    pass


class RegistyException(MLMBaseException):
    """Base exception for all registry exceptions."""

    pass
