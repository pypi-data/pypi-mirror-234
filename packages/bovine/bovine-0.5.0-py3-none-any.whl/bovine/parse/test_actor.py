import pytest
import json
from unittest.mock import AsyncMock, MagicMock
from contextlib import asynccontextmanager

from . import Actor


@pytest.mark.parametrize(
    "actor",
    [
        {},
        {"@context": "about:bovine", "id": "https://local/actor"},
        {
            "@context": "about:bovine",
            "id": "https://local/actor",
            "inbox": "https://local/actor/inbox",
        },
        {
            "@context": "about:bovine",
            "id": "https://local/actor",
            "outbox": "https://local/actor/outbox",
        },
        {
            "@context": "about:bovine",
            "id": "https://local/actor",
            "inbox": "https://local/actor/inbox",
            "outbox": ["https://local/actor/outbox", "https://local/actor/another"],
        },
    ],
)
def test_actor_raises_exception(actor):
    with pytest.raises(ValueError):
        Actor(actor)


def test_actor_good_example():
    data = {
        "@context": "about:bovine",
        "id": "https://local/actor",
        "inbox": "https://local/actor/inbox",
        "outbox": "https://local/actor/outbox",
    }
    actor = Actor(data)
    assert isinstance(actor, Actor)

    assert actor.id == "https://local/actor"


@pytest.mark.parametrize(
    "extra",
    [
        {},
        {"preferredUsername": None},
        {"preferredUsername": ""},
        {"preferredUsername": ["alice", "bob"]},
    ],
)
def test_actor_acct_uri_bad_cases(extra):
    data = {
        "@context": "about:bovine",
        "id": "https://local/actor",
        "inbox": "https://local/actor/inbox",
        "outbox": "https://local/actor/outbox",
        **extra,
    }
    actor = Actor(data)
    assert actor.unvalidated_acct_uri is None


@pytest.mark.parametrize(
    "extra",
    [
        {"preferredUsername": "alice"},
        {"preferredUsername": {"@value": "alice", "@language": "@und"}},
    ],
)
def test_actor_acct_uri_good_cases(extra):
    data = {
        "@context": "about:bovine",
        "id": "https://local/actor",
        "inbox": "https://local/actor/inbox",
        "outbox": "https://local/actor/outbox",
        **extra,
    }
    actor = Actor(data)
    assert actor.unvalidated_acct_uri == "acct:alice@local"


async def test_actor_acct_uri_validation_good():
    data = {
        "@context": "about:bovine",
        "id": "https://local/actor",
        "inbox": "https://local/actor/inbox",
        "outbox": "https://local/actor/outbox",
        "preferredUsername": "alice",
    }
    actor = Actor(data)

    response = AsyncMock(__aenter__=AsyncMock())
    response.status = 200
    response.text.return_value = json.dumps(
        {
            "links": [
                {
                    "href": "https://local/actor",
                    "rel": "self",
                    "type": "application/activity+json",
                }
            ],
            "subject": "acct:alice@local",
        }
    )

    @asynccontextmanager
    async def response_context():
        yield response

    session = MagicMock()
    session.get.return_value = response_context()

    await actor.validate_acct_uri(session=session)

    assert "acct:alice@local" in actor.identifiers


async def test_actor_acct_uri_validation_bad():
    data = {
        "@context": "about:bovine",
        "id": "https://local/actor",
        "inbox": "https://local/actor/inbox",
        "outbox": "https://local/actor/outbox",
        "preferredUsername": "alice",
    }
    actor = Actor(data)

    response = AsyncMock(__aenter__=AsyncMock())
    response.status = 200
    response.text.return_value = json.dumps(
        {
            "links": [
                {
                    "href": "https://local/other",
                    "rel": "self",
                    "type": "application/activity+json",
                }
            ],
            "subject": "acct:alice@local",
        }
    )

    @asynccontextmanager
    async def response_context():
        yield response

    session = MagicMock()
    session.get.return_value = response_context()

    await actor.validate_acct_uri(session=session)

    assert "acct:alice@local" not in actor.identifiers
