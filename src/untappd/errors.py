"""Exceptions raised by the Untappd client."""

from __future__ import annotations


class UntappdError(Exception):
    """Base exception for all errors raised by this library."""


class UntappdAuthError(UntappdError):
    """Raised when a call requires an authenticated access token but none is set."""


class UntappdAPIError(UntappdError):
    """Raised when the Untappd API returns an error response.

    Attributes
    ----------
    code:
        The numeric ``meta.code`` returned by the API.
    error_type:
        The ``meta.error_type`` string returned by the API, if any.
    """

    def __init__(
        self, message: str, *, code: int | None = None, error_type: str | None = None
    ) -> None:
        super().__init__(message)
        self.code = code
        self.error_type = error_type


class UntappdNotFoundError(UntappdError):
    """Raised when a lookup by name/address matches no entity."""
