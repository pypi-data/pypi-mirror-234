from . import BovineClient


def test_bovine_client_host():
    actor = BovineClient().with_actor_id("https://domain.tld/users/someone")

    assert actor.host == "domain.tld"
