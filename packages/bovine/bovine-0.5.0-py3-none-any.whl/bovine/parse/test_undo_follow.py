import pytest
from unittest.mock import AsyncMock

from . import Activity

remote_actor = "http://remote/actor"
local_actor = "http://local/actor"


@pytest.mark.parametrize(
    "activity",
    [
        {},
        {"type": "Undo"},
        {"type": "Undo", "object": "something"},
        {"type": "Undo", "object": {}},
        {"type": "Undo", "object": {"type": "Invite"}},
        {"type": "Undo", "object": {"type": "Follow", "id": "http://remote/follow"}},
        {
            "type": "Undo",
            "actor": local_actor,
            "object": {"type": "Follow", "actor": "http://local/actor/two"},
        },
    ],
)
async def test_undo_follow_bad_cases(activity):
    retrieve = AsyncMock()

    follow = await Activity(activity, domain="local").undo_of_follow(retrieve)

    assert follow is None


@pytest.mark.parametrize(
    "activity",
    [
        {
            "type": "Undo",
            "actor": local_actor,
            "object": {"type": "Follow", "object": remote_actor},
        },
        {
            "type": "Undo",
            "actor": {"id": local_actor},
            "object": {"type": "Follow", "object": remote_actor},
        },
        {
            "type": "Undo",
            "actor": local_actor,
            "object": {"type": "Follow", "object": {"id": remote_actor}},
        },
        {
            "type": "Undo",
            "actor": {"id": local_actor},
            "object": {"type": "Follow", "object": {"id": remote_actor}},
        },
    ],
)
async def test_accept_follow_good_case(activity):
    retrieve = AsyncMock()

    follow = await Activity(activity, domain="local").undo_of_follow(retrieve)

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
        "type": "Undo",
        "actor": "http://local/actor",
        "object": "http://local/follow",
    }

    follow = await Activity(activity, domain="local").undo_of_follow(retrieve)

    assert isinstance(follow, Activity)

    retrieve.assert_awaited_once_with("http://local/follow")
