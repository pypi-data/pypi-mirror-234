import pytest
from unittest.mock import AsyncMock

from . import Activity, Object

remote_actor = "http://remote/actor"


@pytest.mark.parametrize(
    "activity",
    [
        {},
        {"type": "Create"},
        {"type": "Create", "object": "something"},
    ],
)
async def test_create_bad_cases(activity):
    retrieve = AsyncMock()

    obj = await Activity(activity, domain="remote").object_for_create(retrieve)

    assert obj is None


@pytest.mark.parametrize(
    "activity",
    [
        {
            "type": "Create",
            "actor": remote_actor,
            "object": {"id": "http://local/object"},
        },
        {
            "type": "Create",
            "actor": remote_actor,
            "object": {
                "id": "http://remote/object",
                "attributedTo": "http://remote/other",
            },
        },
    ],
)
async def test_create_bad_cases_with_exception(activity):
    retrieve = AsyncMock()

    with pytest.raises(ValueError):
        await Activity(activity, domain="remote").object_for_create(retrieve)


@pytest.mark.parametrize(
    "activity",
    [
        {
            "type": "Create",
            "object": {},
        },
        {
            "type": "Create",
            "object": {"type": "Note", "attributedTo": remote_actor},
        },
        {
            "type": "Create",
            "actor": remote_actor,
            "object": {"type": "Note"},
        },
        {
            "type": "Create",
            "actor": remote_actor,
            "object": {"type": "Note", "attributedTo": remote_actor},
        },
        {
            "type": "Create",
            "actor": {"id": remote_actor},
            "object": {"type": "Note", "attributedTo": remote_actor},
        },
        {
            "type": "Create",
            "actor": remote_actor,
            "object": {"type": "Note", "attributedTo": {"id": remote_actor}},
        },
        {
            "type": "Create",
            "actor": {"id": remote_actor},
            "object": {"type": "Note", "attributedTo": {"id": remote_actor}},
        },
    ],
)
async def test_create_good_cases(activity):
    retrieve = AsyncMock()

    obj = await Activity(activity, domain="remote").object_for_create(retrieve)

    assert isinstance(obj, Object)

    retrieve.assert_not_awaited()


async def test_create_with_retrieving_remote_object():
    obj_id = remote_actor + "/object"
    retrieve = AsyncMock(
        return_value={
            "id": obj_id,
            "type": "Note",
            "attributedTo": remote_actor,
            "content": "note",
        }
    )
    activity = {"type": "Create", "actor": remote_actor, "object": obj_id}

    obj = await Activity(activity, domain="remote").object_for_create(retrieve)

    assert isinstance(obj, Object)

    retrieve.assert_awaited_once_with(obj_id)
