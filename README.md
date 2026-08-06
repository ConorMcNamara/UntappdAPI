# UntappdAPI

A small, typed Python client for the [Untappd API v4](https://untappd.com/api/docs).

> **Note on API access:** Untappd has significantly restricted access to its
> public API and no longer issues new API keys freely. This library targets the
> documented v4 endpoints; whether a given call succeeds depends on the access
> your credentials have been granted. The test suite is fully mocked and does
> not hit the live API.

## Installation

```bash
pip install untappd
```

For local development:

```bash
pip install -e ".[dev]"
```

## Usage

The client is organized into namespaces. Read-only lookups only need your
client ID and secret; anything that acts on behalf of a user needs an OAuth
access token.

```python
from untappd import Untappd

client = Untappd(client_id="...", client_secret="...")

# Search and info (no user token required)
client.search.beers("Pliny the Elder")
client.info.beer_by_id("5")
client.search.trending()

# User feeds
client.feed.user_feed("some_user", limit=10)

# Authenticated actions
client.set_access_token("oauth-access-token")
client.friends.pending()
client.friends.accept("some_user")
client.actions.checkin(gmt_offset=-5, timezone="EST", beer_id="5", rating=4.5)
```

The client can also be used as a context manager to close the underlying
HTTP session:

```python
with Untappd(client_id="...", client_secret="...") as client:
    client.search.trending()
```

### Namespaces

| Namespace         | Purpose                                             |
| ----------------- | --------------------------------------------------- |
| `client.search`   | Search beers, breweries, venues; trending beers     |
| `client.info`     | Detailed info for beers, breweries, venues, users   |
| `client.feed`     | Check-in feeds for friends, users, venues, beers    |
| `client.friends`  | Manage friend requests (requires token)             |
| `client.actions`  | Check in beers, comment, toast, wishlist (token)    |
| `client.users`    | A user's badges, friends, wishlist, notifications   |

## Errors

All errors derive from `UntappdError`:

- `UntappdAuthError` — a token-only call was made without an access token.
- `UntappdAPIError` — the API returned an error envelope (`.code`, `.error_type`).
- `UntappdNotFoundError` — a lookup by name/address matched no entity.

## Development

```bash
ruff check src tests   # lint + import sort
mypy                   # strict type check
pytest                 # tests (fully mocked HTTP)
```

`pre-commit install` wires the same checks into your git hooks.

## License

MIT — see [LICENSE](LICENSE).
