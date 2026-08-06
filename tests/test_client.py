from __future__ import annotations

import pytest
import requests
import responses
from tests.conftest import BASE_URL, ok

from untappd import Untappd, UntappdAPIError, UntappdAuthError


@responses.activate
def test_unauthenticated_request_sends_client_credentials(client: Untappd) -> None:
    responses.get(BASE_URL + "beer/trending", json=ok())
    client.search.trending()

    request = responses.calls[0].request
    assert "client_id=id" in request.url
    assert "client_secret=secret" in request.url
    assert "access_token" not in request.url


@responses.activate
def test_authenticated_request_prefers_access_token(auth_client: Untappd) -> None:
    responses.get(BASE_URL + "user/beers/someone", json=ok())
    auth_client.users.distinct_beers("someone")

    request = responses.calls[0].request
    assert "access_token=token" in request.url
    assert "client_id" not in request.url


def test_token_required_call_without_token_raises(client: Untappd) -> None:
    with pytest.raises(UntappdAuthError):
        client.friends.pending()


def test_set_access_token(client: Untappd) -> None:
    client.set_access_token("later")
    assert client.access_token == "later"


@responses.activate
def test_none_params_are_dropped(client: Untappd) -> None:
    responses.get(BASE_URL + "search/beer", json=ok())
    client.search.beers("ipa")

    request = responses.calls[0].request
    assert "q=ipa" in request.url
    assert "sort" not in request.url
    assert "brewery_name" not in request.url


@responses.activate
def test_api_error_code_raises(client: Untappd) -> None:
    responses.get(
        BASE_URL + "beer/trending",
        json={"meta": {"code": 500, "error_type": "invalid_auth"}},
    )
    with pytest.raises(UntappdAPIError) as exc_info:
        client.search.trending()
    assert exc_info.value.code == 500
    assert exc_info.value.error_type == "invalid_auth"


@responses.activate
def test_http_error_status_raises(client: Untappd) -> None:
    responses.get(BASE_URL + "beer/trending", status=404, json={})
    with pytest.raises(requests.HTTPError):
        client.search.trending()


def test_context_manager_closes_session(client: Untappd) -> None:
    with client as c:
        assert c is client
