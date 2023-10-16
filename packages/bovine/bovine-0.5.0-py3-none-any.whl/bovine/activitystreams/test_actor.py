from bovine.types import Visibility

from . import Actor


def test_actor() -> None:
    actor = Actor(id="http://example.com/actor/123")

    result = actor.build()

    assert set(result.keys()) == {"type", "id", "@context", "outbox", "inbox"}

    actor.name = "John Doe"
    result = actor.build()
    assert set(result.keys()) == {"type", "id", "name", "@context", "outbox", "inbox"}

    actor.public_key = "01234567890123456"
    actor.public_key_name = "key"
    result = actor.build()

    assert set(result.keys()) == {
        "type",
        "id",
        "name",
        "@context",
        "publicKey",
        "outbox",
        "inbox",
    }

    assert result["publicKey"] == {
        "id": actor.id + "#key",
        "owner": actor.id,
        "publicKeyPem": actor.public_key,
    }


def test_actor_second() -> None:
    actor = Actor(id="http://example.com/actor/123", inbox="inbox", outbox="outbox")

    result = actor.build()

    assert result["inbox"] == "inbox"
    assert result["outbox"] == "outbox"

    actor.proxy_url = "http://example.com/proxy"
    result = actor.build(visibility=Visibility.OWNER)

    assert result["endpoints"]["proxyUrl"] == "http://example.com/proxy"


def test_actor_with_icon() -> None:
    actor = Actor(id="http://example.com/actor/123", inbox="inbox", outbox="outbox")
    actor.icon = {"type": "Image"}

    result = actor.build()

    assert result["icon"] == {"type": "Image"}
