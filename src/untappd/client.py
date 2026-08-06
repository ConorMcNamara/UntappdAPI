"""The main Untappd API client."""

from __future__ import annotations

from typing import Any

import requests

from .errors import UntappdAPIError, UntappdAuthError, UntappdNotFoundError
from .resources.actions import Actions
from .resources.feed import Feed
from .resources.friends import Friends
from .resources.info import Info
from .resources.search import Search
from .resources.users import Users

DEFAULT_BASE_URL = "https://api.untappd.com/v4/"
DEFAULT_TIMEOUT = 30.0


class Untappd:
    """Client for the Untappd API v4.

    A single client holds the HTTP session and authentication, and exposes the
    API grouped into namespaces::

        client = Untappd(client_id="...", client_secret="...")
        client.search.beers("Pliny the Elder")
        client.info.beer_by_id("5")

        # Calls that act on behalf of a user need an access token:
        client.set_access_token(token)
        client.friends.accept("some_user")

    Parameters
    ----------
    client_id:
        The Untappd API client ID.
    client_secret:
        The Untappd API client secret.
    access_token:
        An OAuth access token obtained after user authorization. Required for
        any call that acts on behalf of a user. May be set later with
        :meth:`set_access_token`.
    base_url:
        The API base URL. Overridable mainly for testing.
    timeout:
        Per-request timeout in seconds.
    session:
        An existing :class:`requests.Session` to reuse. One is created if not
        provided.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        *,
        access_token: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        session: requests.Session | None = None,
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.base_url = base_url if base_url.endswith("/") else base_url + "/"
        self.timeout = timeout
        self._session = session or requests.Session()

        # Namespaces
        self.search = Search(self)
        self.feed = Feed(self)
        self.friends = Friends(self)
        self.info = Info(self)
        self.actions = Actions(self)
        self.users = Users(self)

    def set_access_token(self, access_token: str) -> None:
        """Set the OAuth access token used for authenticated calls."""
        self.access_token = access_token

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._session.close()

    def __enter__(self) -> Untappd:
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()

    # -- HTTP -----------------------------------------------------------------

    def _auth_params(self, *, require_token: bool) -> dict[str, str]:
        """Build the authentication query parameters for a request."""
        if self.access_token:
            return {"access_token": self.access_token}
        if require_token:
            raise UntappdAuthError(
                "This call acts on behalf of a user and requires an access token; "
                "call set_access_token() first."
            )
        return {"client_id": self.client_id, "client_secret": self.client_secret}

    def _request(
        self,
        http_method: str,
        method: str,
        *,
        params: dict[str, Any] | None = None,
        require_token: bool = False,
    ) -> dict[str, Any]:
        """Send a request to the Untappd API and return the parsed JSON body.

        Parameters
        ----------
        http_method:
            ``"GET"`` or ``"POST"``.
        method:
            The Untappd API method/path, e.g. ``"search/beer"``.
        params:
            Query parameters for the request. ``None`` values are dropped.
        require_token:
            When ``True``, the call requires an authenticated access token.
        """
        query: dict[str, Any] = {
            k: v for k, v in (params or {}).items() if v is not None
        }
        query.update(self._auth_params(require_token=require_token))

        response = self._session.request(
            http_method,
            self.base_url + method,
            params=query,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data: dict[str, Any] = response.json()

        meta = data.get("meta", {})
        code = meta.get("code")
        if code is not None and code >= 400:
            message = (
                meta.get("error_detail")
                or meta.get("error_type")
                or "Untappd API error"
            )
            raise UntappdAPIError(
                message, code=code, error_type=meta.get("error_type")
            )
        return data

    def _get(
        self,
        method: str,
        *,
        params: dict[str, Any] | None = None,
        require_token: bool = False,
    ) -> dict[str, Any]:
        return self._request("GET", method, params=params, require_token=require_token)

    def _post(
        self,
        method: str,
        *,
        params: dict[str, Any] | None = None,
        require_token: bool = False,
    ) -> dict[str, Any]:
        return self._request("POST", method, params=params, require_token=require_token)

    # -- Name -> ID helpers ---------------------------------------------------

    def _find_venue_id(self, venue_name: str, address: str) -> str:
        """Return the venue id for a venue matching ``venue_name`` and ``address``."""
        data = self.search.venues(venue_name)
        items = data["response"]["venues"]["items"]
        for item in items:
            if item.get("venue_address") == address:
                return str(item["venue_id"])
        raise UntappdNotFoundError(
            f"No venue named {venue_name!r} found at address {address!r}"
        )

    def _find_beer_id(self, beer_name: str, brewery_name: str) -> str:
        """Return the beer id for a beer matching ``beer_name`` and ``brewery_name``."""
        data = self.search.beers(beer_name, brewery_name=brewery_name)
        items = data["response"]["beers"]["items"]
        if not items:
            raise UntappdNotFoundError(
                f"No beer named {beer_name!r} from brewery {brewery_name!r}"
            )
        return str(items[0]["beer"]["bid"])

    def _find_brewery_id(self, brewery_name: str) -> str:
        """Return the brewery id for a brewery matching ``brewery_name``."""
        data = self.search.breweries(brewery_name)
        items = data["response"]["brewery"]["items"]
        if not items:
            raise UntappdNotFoundError(f"No brewery named {brewery_name!r}")
        return str(items[0]["brewery"]["brewery_id"])
