import pytest

from .bovine_object import BovineObject


def test_invalid_context():
    with pytest.raises(ValueError):
        BovineObject({"@context": "https://www.w3.org/ns/activitystreams"})


@pytest.mark.parametrize(
    ("obj", "domain"),
    [({}, None), ({"type": "Note"}, None), ({"id": "https://remote"}, "local")],
)
def test_invalid_id_domain(obj, domain):
    with pytest.raises(ValueError):
        BovineObject(obj, domain=domain)


def test_correctly_parses_domain():
    bovine_object = BovineObject({"id": "https://remote"})

    assert bovine_object.domain == "remote"


@pytest.mark.parametrize(
    ("obj", "actor_id"),
    [
        ({}, None),
        ({"type": "Note"}, None),
        ({"actor": None}, None),
        ({"actor": {"type": "Actor"}}, None),
        ({"actor": "http://local/actor"}, "http://local/actor"),
        ({"actor": {"id": "http://local/actor"}}, "http://local/actor"),
    ],
)
def test_actor_id(obj, actor_id):
    bovine_object = BovineObject(obj, domain="local")

    if actor_id is None:
        assert bovine_object.actor_id is None
    else:
        assert bovine_object.actor_id == actor_id


@pytest.mark.parametrize(
    "obj",
    [
        {"actor": "http://remote/actor"},
        {"actor": {"id": "http://remote/actor"}},
    ],
)
def test_actor_id_error_on_different_domain(obj):
    bovine_object = BovineObject(obj, domain="local")

    with pytest.raises(ValueError):
        _ = bovine_object.actor_id


@pytest.mark.parametrize(
    ("obj", "object_id"),
    [
        ({}, None),
        ({"object": {}}, None),
        ({"something": "else"}, None),
        ({"object": "https://remote/object"}, "https://remote/object"),
        ({"object": "https://local/object"}, "https://local/object"),
        ({"object": {"id": "https://remote/object"}}, "https://remote/object"),
        ({"object": {"id": "https://local/object"}}, "https://local/object"),
    ],
)
def test_object_id(obj, object_id):
    bovine_object = BovineObject(obj, domain="local")

    if object_id is None:
        assert bovine_object.object_id is None
    else:
        assert bovine_object.object_id == object_id
