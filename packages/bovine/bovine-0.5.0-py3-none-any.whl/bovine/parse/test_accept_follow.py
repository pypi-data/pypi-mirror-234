import pytest
from unittest.mock import AsyncMock

from . import Activity

remote_actor = "http://remote/actor"


@pytest.mark.parametrize(
    "activity",
    [
        {},
        {"type": "Accept"},
        {"type": "Accept", "object": "something"},
        {"type": "Accept", "object": {}},
        {"type": "Accept", "object": {"type": "Invite"}},
        {
            "type": "Accept",
            "actor": "http://local/actor",
            "object": {"type": "Follow", "object": "remote"},
        },
        {
            "type": "Accept",
            "actor": {"id": "http://local/actor"},
            "object": {"type": "Follow", "object": "remote"},
        },
        {
            "type": "Accept",
            "actor": {"id": "http://local/actor"},
            "object": {"type": "Follow", "object": {"id": "remote"}},
        },
    ],
)
async def test_accept_follow_bad_cases(activity):
    retrieve = AsyncMock()

    follow = await Activity(activity, domain="local").accept_for_follow(retrieve)

    assert follow is None


@pytest.mark.parametrize(
    "activity",
    [
        {
            "type": "Accept",
            "actor": remote_actor,
            "object": {"type": "Follow", "object": remote_actor},
        },
        {
            "type": "Accept",
            "actor": {"id": remote_actor},
            "object": {"type": "Follow", "object": remote_actor},
        },
        {
            "type": "Accept",
            "actor": remote_actor,
            "object": {"type": "Follow", "object": {"id": remote_actor}},
        },
        {
            "type": "Accept",
            "actor": {"id": remote_actor},
            "object": {"type": "Follow", "object": {"id": remote_actor}},
        },
    ],
)
async def test_accept_follow_good_case(activity):
    retrieve = AsyncMock()

    follow = await Activity(activity, domain="remote").accept_for_follow(retrieve)

    assert isinstance(follow, Activity)

    retrieve.assert_not_awaited()


async def test_accept_follow_good_case_with_retrieve():
    retrieve = AsyncMock(
        return_value={
            "id": "http://local/follow",
            "type": "Follow",
            "object": "http://remote/actor",
        }
    )
    activity = {
        "type": "Accept",
        "actor": "http://remote/actor",
        "object": "http://local/follow",
    }

    follow = await Activity(activity, domain="remote").accept_for_follow(retrieve)

    assert isinstance(follow, Activity)

    retrieve.assert_awaited_once_with("http://local/follow")
