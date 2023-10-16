from unittest.mock import AsyncMock, MagicMock, patch

from . import (
    build_validate_http_signature,
    generate_rsa_public_private_key,
    private_key_to_did_key,
    validate_moo_auth_signature,
)
from .test import public_key


def test_generate_rsa_public_private_key():
    public_key, private_key = generate_rsa_public_private_key()

    assert public_key.startswith("-----BEGIN PUBLIC KEY-----")
    assert public_key.endswith("-----END PUBLIC KEY-----\n")

    assert private_key.startswith("-----BEGIN PRIVATE KEY-----")
    assert private_key.endswith("-----END PRIVATE KEY-----\n")


def test_private_key_to_did_key():
    private_key = "z3u2Yxcowsarethebestcowsarethebestcowsarethebest"

    did_key = private_key_to_did_key(private_key)

    assert did_key == "did:key:z6MkekwC6R9bj9ErToB7AiZJfyCSDhaZe1UxhDbCqJrhqpS5"


@patch("bovine.utils.date.check_max_offset_now")
async def test_validate_moo_auth_signature_get(mock_offset):
    # https://blog.mymath.rocks/2023-03-15/BIN1_Moo_Authentication_and_Authoriation#appendix-test-data

    mock_offset.return_value = True

    request = MagicMock(
        method="get",
        path="/path/to/resource",
        headers={
            "date": "Wed, 15 Mar 2023 17:28:15 GMT",
            "host": "myhost.tld",
            "authorization": "Moo-Auth-1 did:key:z6MkekwC6R9bj9ErToB7AiZJfyCSDhaZe1UxhDbCqJrhqpS5",  # noqa F501
            "x-moo-signature": "z5ahdHCbP9aJEsDtvG1MEZpxPzuvGKYcdXdKvMq5YL21Z2umxjs1SopCY2Ap8vZxVjTEf6dYbGuB7mtgcgUyNdBLe",  # noqa F501
        },
    )

    result, _ = await validate_moo_auth_signature(request, "myhost.tld")

    assert result == "did:key:z6MkekwC6R9bj9ErToB7AiZJfyCSDhaZe1UxhDbCqJrhqpS5"


@patch("bovine.utils.date.check_max_offset_now")
async def test_validate_moo_auth_signature_post(mock_offset):
    # https://blog.mymath.rocks/2023-03-15/BIN1_Moo_Authentication_and_Authoriation#appendix-test-data

    mock_offset.return_value = True

    request = MagicMock(
        method="post",
        path="/path/to/resource",
        headers={
            "date": "Wed, 15 Mar 2023 17:28:15 GMT",
            "host": "myhost.tld",
            "authorization": "Moo-Auth-1 did:key:z6MkekwC6R9bj9ErToB7AiZJfyCSDhaZe1UxhDbCqJrhqpS5",  # noqa F501
            "digest": "sha-256=MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k=",
            "x-moo-signature": "z4vPkJaoaSVQp5DrMb8EvCajJcerW36rsyWDELTWQ3cYmaonnGfb8WHiwH54BShidCcmpoyHjanVRYNrXXXka4jAn",  # noqa F501
        },
        get_data=AsyncMock(return_value='{"cows": "good"}'),
    )

    result, _ = await validate_moo_auth_signature(request, "myhost.tld")

    assert result == "did:key:z6MkekwC6R9bj9ErToB7AiZJfyCSDhaZe1UxhDbCqJrhqpS5"


@patch("bovine.utils.date.check_max_offset_now")
async def test_build_validate_http_signature(mock_offset):
    async def key_retriever(url):
        return public_key, "owner"

    mock_offset.return_value = True

    validate_http_signature = build_validate_http_signature(key_retriever)

    request = MagicMock(
        method="get",
        path="/path/to/resource",
        url="https://myhost.tld/path/to/resource",
        headers={
            "date": "Wed, 15 Mar 2023 17:28:15 GMT",
            "host": "myhost.tld",
            "signature": 'keyId="key_id",algorithm="rsa-sha256",headers="(request-target) host date",signature="bwgA3UajpDzM07wM+MUkpGHS/mAhhTu+WDiBL1H28J762jUUuggzP8We5+I0WHypSBCWt8Lap2AbYqG6PfTsdFEbk8VWewX34n7/LUSM/WJeA8AFCEnHYPd8rRib4d0+kQV+U4Ai997XUxs2xi2AruNdkB6SNMkSbnQLoBjYT4tzGaf2I1xZuqjD1HvvW0xa1o/nPt4G5kj0tVmgDrrgeKL2hUJ21UdHcXDNFw9QJWf/O6KyEmbumvppKGFUfdpKSh3n2/fP7O4BxqadCbMYj0oDDOF1H3Pa6GV9EfIeSXXLS9TfyPpkXwbWrNpzUBZQ2hRGzX2jS/JEhpSNSVqv6A=="',  # noqa F501
        },
    )

    assert await validate_http_signature(request)


@patch("bovine.utils.date.check_max_offset_now")
async def test_build_validate_http_signature_post(mock_offset):
    async def key_retriever(url):
        return public_key, "owner"

    mock_offset.return_value = True

    validate_http_signature = build_validate_http_signature(key_retriever)

    request = MagicMock(
        method="post",
        path="/path/to/resource",
        url="https://myhost.tld/path/to/resource",
        headers={
            "date": "Wed, 15 Mar 2023 17:28:15 GMT",
            "host": "myhost.tld",
            "digest": "sha-256=MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k=",
            "signature": 'keyId="key_id",algorithm="rsa-sha256",headers="(request-target) host date digest",signature="QpeLMEh/Z009DgYcSOkrsKr9zW7Wu7UWTQ398qvueCzaEL/Hxrv9C42U+WY/O34x/385lT+z1I3Bk6qMZTDAZSmKGYB5lZJVBdC20a4D++HzIyE62d6CvqUsQwIv4od/hOmmOQ3HKI69MUOsNrLyjIQxUaLSBz1m/wkLv8iMrh9QwULlqTO8WHVjSJlgVwllRtOOcm3wzo/cr2XyFj4gB8CUd3aG3dqzCfOOoNQvUhMDlxP7UqBnGoF6pnYnTnJUSSHdceWbE09TqXLmAHzauYGSdaHRS3XR/Sje7ET9UaOgHHcPJHIN+4jrBpDp2GM69joXWkZwhE0GOl9q3KBSKA=="',  # noqa F501
        },
        get_data=AsyncMock(return_value='{"cows": "good"}'),
    )

    assert await validate_http_signature(request)
