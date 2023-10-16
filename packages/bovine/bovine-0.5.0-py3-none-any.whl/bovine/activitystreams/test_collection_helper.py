import pytest

from bovine import BovineClient

from .collection_helper import CollectionHelper


@pytest.mark.skip("requires instance requests")
async def test_collections():
    # remote = "https://metalhead.club/users/mariusor/following"
    # remote = "FIXME"
    remote = "https://mastodon.social/users/the_milkman/outbox"

    async with BovineClient.from_file("bovine_user.toml") as client:
        collection_helper = CollectionHelper(remote, client, resolve=False)

        async for item in collection_helper:
            print(item)
