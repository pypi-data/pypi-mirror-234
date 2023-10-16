import json

from .helper import content_digest_sha256
from .http_signature import HttpSignature, build_signature
from .test import private_key


def test_http_signature():
    http_signature = HttpSignature().with_field("name", "value")

    signature_string = http_signature.build_signature("key_id", private_key)

    key_id, algorithm, headers, signature = signature_string.split(",")

    assert key_id == 'keyId="key_id"'
    assert algorithm == 'algorithm="rsa-sha256"'
    assert headers == 'headers="name"'
    assert (
        signature
        == 'signature="vpuy8U8A9w7Pr03956AaGg6VaLdZ6FTZuO6bsPL01SI1IIJj32mM/OCutktf0Fkqm1e1qcjDO6EVe3wZWRMjBN0GjE7NTj9wm8rBCQstdowVrwduHTuyPzWKzyoE+u7xBZPXwKy3uy1blC2BH4DJybZ94Hy2z+emrh3XKm+pi0xmMTdACvhizSP+inKHVbolFJ+zxj63wp/6AtkqzQEHbZq8X2DN1mIoDRMA4tPk0q9s5XMb02LyR1fNx5UeA2H/bijvgKY5OvstWbMXcUcPGVUA9elkPT23RNaCch63iaF1dmo/ke8JXy9zFZNx2UfmAO9yEclf6Azcz3kWy0SSQA=="'  # noqa F501
    )


def test_build_signature():
    http_signature = http_signature = build_signature(
        "myhost.tld", "get", "/path/to/resource"
    ).with_field("date", "Wed, 15 Mar 2023 17:28:15 GMT")

    signature_string = http_signature.build_signature("key_id", private_key)

    assert (
        signature_string
        == 'keyId="key_id",algorithm="rsa-sha256",headers="(request-target) host date",signature="bwgA3UajpDzM07wM+MUkpGHS/mAhhTu+WDiBL1H28J762jUUuggzP8We5+I0WHypSBCWt8Lap2AbYqG6PfTsdFEbk8VWewX34n7/LUSM/WJeA8AFCEnHYPd8rRib4d0+kQV+U4Ai997XUxs2xi2AruNdkB6SNMkSbnQLoBjYT4tzGaf2I1xZuqjD1HvvW0xa1o/nPt4G5kj0tVmgDrrgeKL2hUJ21UdHcXDNFw9QJWf/O6KyEmbumvppKGFUfdpKSh3n2/fP7O4BxqadCbMYj0oDDOF1H3Pa6GV9EfIeSXXLS9TfyPpkXwbWrNpzUBZQ2hRGzX2jS/JEhpSNSVqv6A=="'  # noqa F501
    )

    key_id, algorithm, headers, signature = signature_string.split(",")

    assert key_id == 'keyId="key_id"'
    assert algorithm == 'algorithm="rsa-sha256"'
    assert headers == 'headers="(request-target) host date"'
    assert (
        signature
        == 'signature="bwgA3UajpDzM07wM+MUkpGHS/mAhhTu+WDiBL1H28J762jUUuggzP8We5+I0WHypSBCWt8Lap2AbYqG6PfTsdFEbk8VWewX34n7/LUSM/WJeA8AFCEnHYPd8rRib4d0+kQV+U4Ai997XUxs2xi2AruNdkB6SNMkSbnQLoBjYT4tzGaf2I1xZuqjD1HvvW0xa1o/nPt4G5kj0tVmgDrrgeKL2hUJ21UdHcXDNFw9QJWf/O6KyEmbumvppKGFUfdpKSh3n2/fP7O4BxqadCbMYj0oDDOF1H3Pa6GV9EfIeSXXLS9TfyPpkXwbWrNpzUBZQ2hRGzX2jS/JEhpSNSVqv6A=="'  # noqa F501
    )


def test_build_signature_post():
    http_signature = http_signature = (
        build_signature("myhost.tld", "post", "/path/to/resource")
        .with_field("date", "Wed, 15 Mar 2023 17:28:15 GMT")
        .with_field("digest", "sha-256=MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k=")
    )

    signature_string = http_signature.build_signature("key_id", private_key)

    assert (
        signature_string
        == 'keyId="key_id",algorithm="rsa-sha256",headers="(request-target) host date digest",signature="QpeLMEh/Z009DgYcSOkrsKr9zW7Wu7UWTQ398qvueCzaEL/Hxrv9C42U+WY/O34x/385lT+z1I3Bk6qMZTDAZSmKGYB5lZJVBdC20a4D++HzIyE62d6CvqUsQwIv4od/hOmmOQ3HKI69MUOsNrLyjIQxUaLSBz1m/wkLv8iMrh9QwULlqTO8WHVjSJlgVwllRtOOcm3wzo/cr2XyFj4gB8CUd3aG3dqzCfOOoNQvUhMDlxP7UqBnGoF6pnYnTnJUSSHdceWbE09TqXLmAHzauYGSdaHRS3XR/Sje7ET9UaOgHHcPJHIN+4jrBpDp2GM69joXWkZwhE0GOl9q3KBSKA=="'  # noqa F501
    )


def test_build_message():
    http_signature = build_signature(
        "myhost.tld", "get", "/path/to/resource"
    ).with_field("date", "Wed, 15 Mar 2023 17:28:15 GMT")

    message = http_signature.build_message()

    assert (
        message
        == """(request-target): get /path/to/resource
host: myhost.tld
date: Wed, 15 Mar 2023 17:28:15 GMT"""
    )

    signature = http_signature.ed25519_sign(
        "z3u2Yxcowsarethebestcowsarethebestcowsarethebest"
    )

    assert (
        signature
        == "z5ahdHCbP9aJEsDtvG1MEZpxPzuvGKYcdXdKvMq5YL21Z2"
        + "umxjs1SopCY2Ap8vZxVjTEf6dYbGuB7mtgcgUyNdBLe"
    )

    didkey = "did:key:z6MkekwC6R9bj9ErToB7AiZJfyCSDhaZe1UxhDbCqJrhqpS5"

    http_signature.ed25519_verify(didkey, signature)


def test_build_message_post():
    body = json.dumps({"cows": "good"}).encode("utf-8")

    assert body == b'{"cows": "good"}'

    digest = content_digest_sha256(body)

    assert digest == "sha-256=MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k="

    http_signature = (
        build_signature("myhost.tld", "post", "/path/to/resource")
        .with_field("date", "Wed, 15 Mar 2023 17:28:15 GMT")
        .with_field("digest", digest)
    )

    message = http_signature.build_message()

    assert (
        message
        == """(request-target): post /path/to/resource
host: myhost.tld
date: Wed, 15 Mar 2023 17:28:15 GMT
digest: sha-256=MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k="""
    )

    signature = http_signature.ed25519_sign(
        "z3u2Yxcowsarethebestcowsarethebestcowsarethebest"
    )

    assert (
        signature
        == "z4vPkJaoaSVQp5DrMb8EvCajJcerW36rsyWDELTWQ3cYmaonnGf"
        + "b8WHiwH54BShidCcmpoyHjanVRYNrXXXka4jAn"
    )

    didkey = "did:key:z6MkekwC6R9bj9ErToB7AiZJfyCSDhaZe1UxhDbCqJrhqpS5"

    http_signature.ed25519_verify(didkey, signature)
