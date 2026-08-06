from __future__ import annotations

import pytest

from untappd import Untappd

BASE_URL = "https://api.untappd.com/v4/"


@pytest.fixture
def client() -> Untappd:
    return Untappd(client_id="id", client_secret="secret")


@pytest.fixture
def auth_client() -> Untappd:
    return Untappd(client_id="id", client_secret="secret", access_token="token")


def ok(response: dict | None = None, code: int = 200) -> dict:
    """Build a well-formed Untappd API envelope."""
    return {"meta": {"code": code}, "response": response or {}}
