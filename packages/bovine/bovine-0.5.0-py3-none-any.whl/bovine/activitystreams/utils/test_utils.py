from bovine.activitystreams.object_factory import Object

from . import (
    actor_for_object,
    fediverse_handle_from_actor,
    is_public,
    recipients_for_object,
)


def test_get_recipients():
    note = Object(
        type="Note", attributed_to="account", followers="account/followers"
    ).as_public()
    note.cc.add("cc")
    note.to.add("to")
    note.to.add("same")
    note.cc.add("same")
    note = note.build()

    recipients = recipients_for_object(note)

    assert recipients == {
        "account/followers",
        "https://www.w3.org/ns/activitystreams#Public",
        "cc",
        "to",
        "same",
    }


def test_is_public():
    note = (
        Object(type="Note", attributed_to="account", followers="account/followers")
        .as_public()
        .build()
    )
    assert is_public(note)

    note = Object(
        type="Note", attributed_to="account", followers="account/followers"
    ).build()
    assert not is_public(note)

    note = Object(type="Note", attributed_to="account", followers="account/followers")
    note.cc.add("someone")
    note = note.build()
    assert not is_public(note)

    note = (
        Object(type="Note", attributed_to="account", followers="account/followers")
        .as_unlisted()
        .build()
    )
    assert is_public(note)

    note = Object(
        type="Note", attributed_to="account", followers="account/followers"
    ).build()
    note["to"] = "as:Public"
    assert is_public(note)


def test_actor_for_object():
    assert actor_for_object({}) == "__NO__ACTOR__"
    assert actor_for_object({"actor": "alice"}) == "alice"
    assert actor_for_object({"actor": {"id": "alice"}}) == "alice"
    assert actor_for_object({"actor": {}}) == "__NO__ACTOR__"
    assert actor_for_object({"attributedTo": "alice"}) == "alice"
    assert actor_for_object({"attributedTo": {"id": "alice"}}) == "alice"
    assert actor_for_object({"attributedTo": {}}) == "__NO__ACTOR__"


def test_fediverse_handle():
    assert (
        fediverse_handle_from_actor({"id": "https://abel/actor/alice"}) == "alice@abel"
    )
    assert (
        fediverse_handle_from_actor(
            {"id": "https://abel/actor/alice", "preferredUsername": "alyssa"}
        )
        == "alyssa@abel"
    )
