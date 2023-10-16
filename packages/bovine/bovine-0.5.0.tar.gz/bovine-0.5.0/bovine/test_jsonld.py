from .jsonld import (
    split_into_objects,
    use_context,
    value_from_object,
    with_bovine_context,
)


async def test_json_ld_split_one_item():
    first_id = "https://my_domain/first"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
    }

    subobjects = await split_into_objects(item)

    assert subobjects == [item]


async def test_json_ld_split():
    first_id = "https://my_domain/first"
    second_id = "https://my_domain/second"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
        "object": {
            "type": "Note",
            "id": second_id,
        },
    }

    subobjects = await split_into_objects(item)

    first, second = subobjects
    assert first["id"] == first_id
    assert second["id"] == second_id

    assert first["object"] == second_id


async def test_json_ld_split_subobject():
    first_id = "https://my_domain/first"
    second_id = "https://my_domain/second"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
        "object": {
            "type": "Note",
            "id": second_id,
        },
        "tag": [{"type": "Mention"}],
    }

    subobjects = await split_into_objects(item)

    first, second = subobjects
    assert first["id"] == first_id
    assert second["id"] == second_id

    assert first["object"] == second_id
    assert first["tag"] == {"type": "Mention"}


async def test_json_ld_split_subobject_list():
    first_id = "https://my_domain/first"
    second_id = "https://my_domain/second"
    tags = [{"type": "Mention", "name": "one"}, {"type": "Mention", "name": "two"}]
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
        "object": {
            "type": "Note",
            "id": second_id,
        },
        "tag": tags,
    }

    subobjects = await split_into_objects(item)

    first, second = subobjects
    assert first["id"] == first_id
    assert second["id"] == second_id

    assert first["object"] == second_id
    assert first["tag"] == tags


def test_use_context():
    input_jsonld = {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1",
            {
                "manuallyApprovesFollowers": "as:manuallyApprovesFollowers",
                "toot": "http://joinmastodon.org/ns#",
                "featured": {"@id": "toot:featured", "@type": "@id"},
                "featuredTags": {"@id": "toot:featuredTags", "@type": "@id"},
                "alsoKnownAs": {"@id": "as:alsoKnownAs", "@type": "@id"},
                "movedTo": {"@id": "as:movedTo", "@type": "@id"},
                "schema": "http://schema.org#",
                "PropertyValue": "schema:PropertyValue",
                "value": "schema:value",
                "discoverable": "toot:discoverable",
                "Device": "toot:Device",
                "Ed25519Signature": "toot:Ed25519Signature",
                "Ed25519Key": "toot:Ed25519Key",
                "Curve25519Key": "toot:Curve25519Key",
                "EncryptedMessage": "toot:EncryptedMessage",
                "publicKeyBase64": "toot:publicKeyBase64",
                "deviceId": "toot:deviceId",
                "claim": {"@type": "@id", "@id": "toot:claim"},
                "fingerprintKey": {"@type": "@id", "@id": "toot:fingerprintKey"},
                "identityKey": {"@type": "@id", "@id": "toot:identityKey"},
                "devices": {"@type": "@id", "@id": "toot:devices"},
                "messageFranking": "toot:messageFranking",
                "messageType": "toot:messageType",
                "cipherText": "toot:cipherText",
                "suspended": "toot:suspended",
                "Hashtag": "as:Hashtag",
                "focalPoint": {"@container": "@list", "@id": "toot:focalPoint"},
            },
        ],
        "id": "https://somewhere.social/users/someone#main-key",
        "owner": "https://somewhere.social/users/someone",
        "publicKeyPem": """-----BEGIN PUBLIC KEY-----
        XXXXXXXXXXXXXXXXX
        XXXXXXXXXXXXXXXXX
        XXXXXXXXXXXXXXXXX
        XXXXXXXXXXXXXXXXX
        -----END PUBLIC KEY-----
        """,
    }

    output_jsonld = use_context(
        input_jsonld,
        ["https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1"],
    )

    assert output_jsonld == {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1",
        ],
        "id": "https://somewhere.social/users/someone#main-key",
        "owner": "https://somewhere.social/users/someone",
        "publicKeyPem": """-----BEGIN PUBLIC KEY-----
        XXXXXXXXXXXXXXXXX
        XXXXXXXXXXXXXXXXX
        XXXXXXXXXXXXXXXXX
        XXXXXXXXXXXXXXXXX
        -----END PUBLIC KEY-----
        """,
    }


def test_value_from_object():
    value = "my value"
    key = "my_key"

    assert value_from_object({}, key) is None

    assert value == value_from_object({"my_key": value}, key)
    assert value == value_from_object({"my_key": {"@value": value}}, key)


def test_bovine_context():
    data = {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1",
        ],
        "id": "https://bovine.social/activitypub/bovine#main-key",
        "owner": "https://bovine.social/activitypub/bovine",
        "publicKeyPem": """-----BEGIN PUBLIC KEY-----
        ...
        -----END PUBLIC KEY-----""",
    }

    transformed = with_bovine_context(data)

    data["@context"] = "about:bovine"

    assert transformed == data
