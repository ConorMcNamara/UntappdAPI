"""Check-in feed endpoints."""

from __future__ import annotations

from typing import Any

from . import Resource


class Feed(Resource):
    """Retrieve check-in feeds for friends, users, venues, beers and breweries."""

    def friend_feed(
        self, *, max_id: str | None = None, limit: int | None = None
    ) -> dict[str, Any]:
        """Return the authenticated user's friend check-in feed.

        Requires an access token.
        """
        return self._client._get(
            "checkin/recent",
            params={"max_id": max_id, "limit": limit},
            require_token=True,
        )

    def user_feed(
        self,
        username: str,
        *,
        max_id: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """Return the check-in feed of ``username``."""
        return self._client._get(
            f"user/checkin/{username}",
            params={"max_id": max_id, "limit": limit},
        )

    def pub_feed(
        self,
        *,
        min_id: str | None = None,
        lng: str | None = None,
        lat: str | None = None,
        radius: int | None = None,
        max_id: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """Return the public check-in feed for a location."""
        return self._client._get(
            "thepub/local",
            params={
                "min_id": min_id,
                "lng": lng,
                "lat": lat,
                "radius": radius,
                "max_id": max_id,
                "limit": limit,
            },
        )

    def venue_feed_by_id(
        self,
        venue_id: str,
        *,
        min_id: int | None = None,
        max_id: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """Return the check-in feed of a venue by id."""
        return self._client._get(
            f"venue/checkins/{venue_id}",
            params={"min_id": min_id, "max_id": max_id, "limit": limit},
        )

    def venue_feed_by_name(
        self,
        venue_name: str,
        address: str,
        *,
        min_id: int | None = None,
        max_id: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """Return the check-in feed of a venue by name and address."""
        venue_id = self._client._find_venue_id(venue_name, address)
        return self.venue_feed_by_id(
            venue_id, min_id=min_id, max_id=max_id, limit=limit
        )

    def beer_feed_by_id(
        self,
        beer_id: str,
        *,
        min_id: int | None = None,
        max_id: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """Return the check-in feed of a beer by id."""
        return self._client._get(
            f"beer/checkins/{beer_id}",
            params={"min_id": min_id, "max_id": max_id, "limit": limit},
        )

    def beer_feed_by_name(
        self,
        beer_name: str,
        brewery_name: str,
        *,
        min_id: int | None = None,
        max_id: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """Return the check-in feed of a beer by name and brewery."""
        beer_id = self._client._find_beer_id(beer_name, brewery_name)
        return self.beer_feed_by_id(beer_id, min_id=min_id, max_id=max_id, limit=limit)

    def brewery_feed_by_id(
        self,
        brewery_id: str,
        *,
        min_id: int | None = None,
        max_id: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """Return the check-in feed of a brewery by id."""
        return self._client._get(
            f"brewery/checkins/{brewery_id}",
            params={"min_id": min_id, "max_id": max_id, "limit": limit},
        )

    def brewery_feed_by_name(
        self,
        brewery_name: str,
        *,
        min_id: int | None = None,
        max_id: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """Return the check-in feed of a brewery by name."""
        brewery_id = self._client._find_brewery_id(brewery_name)
        return self.brewery_feed_by_id(
            brewery_id, min_id=min_id, max_id=max_id, limit=limit
        )
