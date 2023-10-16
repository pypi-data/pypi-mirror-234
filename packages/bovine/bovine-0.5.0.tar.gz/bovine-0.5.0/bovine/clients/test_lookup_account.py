import aiohttp

from . import lookup_account_with_webfinger, lookup_did_with_webfinger, lookup_with_dns


async def test_lookup_account():
    async with aiohttp.ClientSession() as session:
        result = await lookup_account_with_webfinger(session, "helge@mymath.rocks")

    assert result.startswith("https://mymath.rocks/")


async def test_lookup_did_with_webfinger():
    did_helge = "did:key:z6MkujdZ216eYz55vz8X5HetqeJXj9ddn5ZHZUsBpRX4wfnL"
    async with aiohttp.ClientSession() as session:
        result = await lookup_did_with_webfinger(session, "mymath.rocks", did_helge)

    assert result.startswith("https://mymath.rocks/")


async def test_lookup_did_with_webfinger_with_protocol():
    did_helge = "did:key:z6MkujdZ216eYz55vz8X5HetqeJXj9ddn5ZHZUsBpRX4wfnL"
    async with aiohttp.ClientSession() as session:
        result = await lookup_did_with_webfinger(
            session, "https://mymath.rocks", did_helge
        )

    assert result.startswith("https://mymath.rocks/")


async def test_lookup_with_dns():
    domain = "mymath.rocks"

    async with aiohttp.ClientSession() as session:
        result = await lookup_with_dns(session, domain)

    assert (
        result
        == "https://mymath.rocks/endpoints/SYn3cl_N4HAPfPHgo2x37XunLEmhV9LnxCggcYwyec0"
    )


async def test_lookup_with_dns_no_result():
    domain = "duh.mymath.rocks"

    async with aiohttp.ClientSession() as session:
        result = await lookup_with_dns(session, domain)

    assert result is None
