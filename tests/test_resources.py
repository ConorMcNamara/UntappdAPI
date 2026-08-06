from __future__ import annotations

import pytest
import responses
from tests.conftest import BASE_URL, ok

from untappd import Untappd, UntappdNotFoundError
from untappd.resources.actions import MAX_COMMENT_LENGTH, MAX_SHOUT_LENGTH


@responses.activate
def test_search_beers_with_brewery_name(client: Untappd) -> None:
    responses.get(BASE_URL + "search/beer", json=ok())
    client.search.beers("pliny", brewery_name="Russian River")

    url = responses.calls[0].request.url
    assert "q=pliny" in url
    assert "brewery_name=Russian+River" in url


@responses.activate
def test_find_venue_id_matches_address(client: Untappd) -> None:
    search_body = ok(
        {
            "venues": {
                "items": [
                    {"venue_id": 1, "venue_address": "1 Main St"},
                    {"venue_id": 2, "venue_address": "2 Elm St"},
                ]
            }
        }
    )
    responses.get(BASE_URL + "search/venue", json=search_body)
    responses.get(BASE_URL + "venue/info/2", json=ok())

    client.info.venue_by_name("Some Bar", "2 Elm St")

    assert responses.calls[1].request.url.startswith(BASE_URL + "venue/info/2")


@responses.activate
def test_find_venue_id_no_match_raises(client: Untappd) -> None:
    responses.get(
        BASE_URL + "search/venue",
        json=ok({"venues": {"items": [{"venue_id": 1, "venue_address": "1 Main St"}]}}),
    )
    with pytest.raises(UntappdNotFoundError):
        client.info.venue_by_name("Some Bar", "999 Nowhere")


@responses.activate
def test_find_beer_id_empty_raises(client: Untappd) -> None:
    responses.get(BASE_URL + "search/beer", json=ok({"beers": {"items": []}}))
    with pytest.raises(UntappdNotFoundError):
        client.info.beer_by_name("Ghost", "Nonexistent Brewery")


@responses.activate
def test_beer_by_name_resolves_id(client: Untappd) -> None:
    responses.get(
        BASE_URL + "search/beer",
        json=ok({"beers": {"items": [{"beer": {"bid": 42}}]}}),
    )
    responses.get(BASE_URL + "beer/info/42", json=ok())
    client.info.beer_by_name("Pliny", "Russian River")
    assert responses.calls[1].request.url.startswith(BASE_URL + "beer/info/42")


@responses.activate
def test_checkin_includes_rating_and_cross_posts(auth_client: Untappd) -> None:
    responses.post(BASE_URL + "checkin/add", json=ok())
    auth_client.actions.checkin(
        gmt_offset=-5, timezone="EST", beer_id="42", rating=4.5, twitter=True
    )
    url = responses.calls[0].request.url
    assert "rating=4.5" in url
    assert "twitter=on" in url
    assert "bid=42" in url


def test_checkin_rejects_long_shout(auth_client: Untappd) -> None:
    with pytest.raises(ValueError, match="shout"):
        auth_client.actions.checkin(
            gmt_offset=0,
            timezone="UTC",
            beer_id="1",
            shout="x" * (MAX_SHOUT_LENGTH + 1),
        )


def test_checkin_rejects_high_rating(auth_client: Untappd) -> None:
    with pytest.raises(ValueError, match="rating"):
        auth_client.actions.checkin(
            gmt_offset=0, timezone="UTC", beer_id="1", rating=6
        )


def test_add_comment_rejects_long_comment(auth_client: Untappd) -> None:
    with pytest.raises(ValueError, match="comment"):
        auth_client.actions.add_comment("1", "x" * (MAX_COMMENT_LENGTH + 1))


@responses.activate
def test_friends_accept_uses_post(auth_client: Untappd) -> None:
    responses.post(BASE_URL + "friend/accept/bob", json=ok())
    auth_client.friends.accept("bob")
    assert responses.calls[0].request.method == "POST"
