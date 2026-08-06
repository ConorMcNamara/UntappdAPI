"""Entity information endpoints for breweries, beers, venues, check-ins and users."""

from __future__ import annotations

from typing import Any

from . import Resource


class Info(Resource):
    """Look up detailed information about Untappd entities."""

    def brewery_by_id(
        self, brewery_id: str, *, compact: bool | None = None
    ) -> dict[str, Any]:
        """Return information about a brewery by id."""
        return self._client._get(
            f"brewery/info/{brewery_id}", params={"compact": compact}
        )

    def brewery_by_name(
        self, brewery_name: str, *, compact: bool | None = None
    ) -> dict[str, Any]:
        """Return information about a brewery by name."""
        brewery_id = self._client._find_brewery_id(brewery_name)
        return self.brewery_by_id(brewery_id, compact=compact)

    def beer_by_id(
        self, beer_id: str, *, compact: bool | None = None
    ) -> dict[str, Any]:
        """Return information about a beer by id."""
        return self._client._get(f"beer/info/{beer_id}", params={"compact": compact})

    def beer_by_name(
        self, beer_name: str, brewery_name: str, *, compact: bool | None = None
    ) -> dict[str, Any]:
        """Return information about a beer by name and brewery."""
        beer_id = self._client._find_beer_id(beer_name, brewery_name)
        return self.beer_by_id(beer_id, compact=compact)

    def venue_by_id(
        self, venue_id: str, *, compact: bool | None = None
    ) -> dict[str, Any]:
        """Return information about a venue by id."""
        return self._client._get(f"venue/info/{venue_id}", params={"compact": compact})

    def venue_by_name(
        self, venue_name: str, address: str, *, compact: bool | None = None
    ) -> dict[str, Any]:
        """Return information about a venue by name and address."""
        venue_id = self._client._find_venue_id(venue_name, address)
        return self.venue_by_id(venue_id, compact=compact)

    def checkin(self, checkin_id: str) -> dict[str, Any]:
        """Return information about a check-in."""
        return self._client._get(f"checkin/view/{checkin_id}")

    def user(self, username: str, *, compact: bool | None = None) -> dict[str, Any]:
        """Return information about a user."""
        return self._client._get(f"user/info/{username}", params={"compact": compact})
