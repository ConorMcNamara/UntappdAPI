"""User-specific information endpoints."""

from __future__ import annotations

from typing import Any

from . import Resource


class Users(Resource):
    """Retrieve a user's badges, friends, wishlist, beers and notifications."""

    def badges(self, username: str, *, offset: int | None = None) -> dict[str, Any]:
        """Return a user's badges. Requires an access token."""
        return self._client._get(
            f"user/badges/{username}", params={"offset": offset}, require_token=True
        )

    def friends(
        self,
        username: str,
        *,
        offset: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """Return a user's friends."""
        return self._client._get(
            f"user/friends/{username}", params={"offset": offset, "limit": limit}
        )

    def wishlist(
        self,
        username: str,
        *,
        sort: str | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Return a user's wishlisted beers."""
        return self._client._get(
            f"user/wishlist/{username}", params={"sort": sort, "offset": offset}
        )

    def distinct_beers(
        self,
        username: str,
        *,
        sort: str | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Return the distinct beers a user has had."""
        return self._client._get(
            f"user/beers/{username}", params={"sort": sort, "offset": offset}
        )

    def notifications(self) -> dict[str, Any]:
        """Return the authenticated user's notifications. Requires an access token."""
        return self._client._get("notifications", require_token=True)
