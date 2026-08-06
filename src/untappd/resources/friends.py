"""Friendship endpoints. All calls require an access token."""

from __future__ import annotations

from typing import Any

from . import Resource


class Friends(Resource):
    """Manage friend requests and friendships for the authenticated user."""

    def pending(self) -> dict[str, Any]:
        """Return the authenticated user's pending friend requests."""
        return self._client._get("user/pending", require_token=True)

    def accept(self, target_user: str) -> dict[str, Any]:
        """Accept a friend request from ``target_user``."""
        return self._client._post(f"friend/accept/{target_user}", require_token=True)

    def reject(self, target_user: str) -> dict[str, Any]:
        """Reject a friend request from ``target_user``."""
        return self._client._post(f"friend/reject/{target_user}", require_token=True)

    def remove(self, target_user: str) -> dict[str, Any]:
        """Remove ``target_user`` from the authenticated user's friends."""
        return self._client._post(f"friend/remove/{target_user}", require_token=True)

    def request(self, target_user: str) -> dict[str, Any]:
        """Send a friend request to ``target_user``."""
        return self._client._post(f"friend/request/{target_user}", require_token=True)
