"""Endpoints that act on behalf of the authenticated user."""

from __future__ import annotations

from typing import Any

from . import Resource

MAX_SHOUT_LENGTH = 256
MAX_COMMENT_LENGTH = 140
MAX_RATING = 5


class Actions(Resource):
    """Perform actions such as checking in beers and managing comments.

    All calls require an access token.
    """

    def checkin(
        self,
        gmt_offset: int,
        timezone: str,
        beer_id: str,
        *,
        foursquare_id: str | None = None,
        geolat: float | None = None,
        geolng: float | None = None,
        shout: str | None = None,
        rating: float | None = None,
        facebook: bool = False,
        twitter: bool = False,
        foursquare: bool = False,
        instagram: bool = False,
    ) -> dict[str, Any]:
        """Check in a beer for the authenticated user.

        Parameters
        ----------
        gmt_offset:
            The numeric offset the user is away from GMT.
        timezone:
            The timezone of the user.
        beer_id:
            The id of the beer being checked in.
        foursquare_id:
            MD5 hash of the venue id.
        geolat, geolng:
            Latitude/longitude of the user; required if adding location.
        shout:
            Comment text for the check-in (max 256 characters).
        rating:
            Numeric rating for the beer (0-5).
        facebook, twitter, foursquare, instagram:
            Whether to cross-post the check-in to each service.
        """
        if shout is not None and len(shout) > MAX_SHOUT_LENGTH:
            raise ValueError(
                f"Check-in shout is {len(shout)} characters; Untappd supports "
                f"up to {MAX_SHOUT_LENGTH}."
            )
        if rating is not None and rating > MAX_RATING:
            raise ValueError(
                f"Check-in rating is {rating}; Untappd supports up to {MAX_RATING}."
            )
        params: dict[str, Any] = {
            "gmt_offset": gmt_offset,
            "timezone": timezone,
            "bid": beer_id,
            "foursquare_id": foursquare_id,
            "geolat": geolat,
            "geolng": geolng,
            "shout": shout,
            "rating": rating,
        }
        for service, enabled in (
            ("facebook", facebook),
            ("twitter", twitter),
            ("foursquare", foursquare),
            ("instagram", instagram),
        ):
            if enabled:
                params[service] = "on"
        return self._client._post("checkin/add", params=params, require_token=True)

    def add_comment(self, checkin_id: str, comment: str) -> dict[str, Any]:
        """Add a comment to a check-in (max 140 characters)."""
        if len(comment) > MAX_COMMENT_LENGTH:
            raise ValueError(
                f"Check-in comment is {len(comment)} characters; Untappd supports "
                f"up to {MAX_COMMENT_LENGTH}."
            )
        return self._client._post(
            f"checkin/addcomment/{checkin_id}",
            params={"comment": comment},
            require_token=True,
        )

    def remove_comment(self, comment_id: str) -> dict[str, Any]:
        """Remove a comment from a check-in."""
        return self._client._post(
            f"checkin/deletecomment/{comment_id}", require_token=True
        )

    def toast(self, checkin_id: str) -> dict[str, Any]:
        """Toggle the toast on a check-in."""
        return self._client._post(f"checkin/toast/{checkin_id}", require_token=True)

    def add_to_wishlist(self, beer_id: str) -> dict[str, Any]:
        """Add a beer to the authenticated user's wishlist."""
        return self._client._get(
            "user/wishlist/add", params={"bid": beer_id}, require_token=True
        )

    def remove_from_wishlist(self, beer_id: str) -> dict[str, Any]:
        """Remove a beer from the authenticated user's wishlist."""
        return self._client._get(
            "user/wishlist/delete", params={"bid": beer_id}, require_token=True
        )
