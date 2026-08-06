"""API resource namespaces."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import Untappd


class Resource:
    """Base class for an API namespace bound to a client."""

    def __init__(self, client: Untappd) -> None:
        self._client = client
