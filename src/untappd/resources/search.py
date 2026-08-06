"""Search and discovery endpoints."""

from __future__ import annotations

from typing import Any

from . import Resource


class Search(Resource):
    """Search for breweries, beers and venues, and browse trending beers."""

    def breweries(self, query: str) -> dict[str, Any]:
        """Return breweries matching ``query``."""
        return self._client._get("search/brewery", params={"q": query})

    def beers(
        self,
        query: str,
        *,
        sort: str | None = None,
        brewery_name: str | None = None,
    ) -> dict[str, Any]:
        """Return beers matching ``query``.

        Parameters
        ----------
        query:
            The search term.
        sort:
            Optional ordering for the results.
        brewery_name:
            Optional brewery name used to narrow the search.
        """
        return self._client._get(
            "search/beer",
            params={"q": query, "sort": sort, "brewery_name": brewery_name},
        )

    def venues(self, query: str, *, sort: str | None = None) -> dict[str, Any]:
        """Return venues matching ``query``."""
        return self._client._get("search/venue", params={"q": query, "sort": sort})

    def foursquare_venue(self, venue_id: str) -> dict[str, Any]:
        """Convert a Foursquare v2 venue ID into an Untappd venue ID."""
        return self._client._get(f"venue/foursquare_lookup/{venue_id}")

    def trending(self) -> dict[str, Any]:
        """Return the trending macro and micro beers."""
        return self._client._get("beer/trending")
