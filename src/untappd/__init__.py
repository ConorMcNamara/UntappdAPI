"""A Python client for the Untappd API v4."""

from __future__ import annotations

from .client import Untappd
from .errors import (
    UntappdAPIError,
    UntappdAuthError,
    UntappdError,
    UntappdNotFoundError,
)

__version__ = "0.1.0"

__all__ = [
    "Untappd",
    "UntappdAPIError",
    "UntappdAuthError",
    "UntappdError",
    "UntappdNotFoundError",
]
