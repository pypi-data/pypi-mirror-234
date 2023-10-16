from typing import Optional
from urllib.parse import urlparse


def actor_for_object(data: dict) -> str:
    """Look up for the actor id either from attributedTo or actor"""
    if "attributedTo" in data:
        actor = data.get("attributedTo")
    else:
        actor = data.get("actor")
    actor = id_for_object(actor)

    if actor:
        return actor

    return "__NO__ACTOR__"


def id_for_object(data: Optional[dict | str]) -> Optional[str]:
    """Determines the id of an object"""

    if data is None:
        return None
    if isinstance(data, str):
        return data
    return data.get("id", None)


def property_for_key_as_set(data, key):
    if data is None:
        return set()
    result = data.get(key, [])
    if isinstance(result, str):
        return set([result])
    return set(result)


def recipients_for_object(data: dict) -> set:
    """Combines the recipients from to, cc, bto, bcc, audience into a set"""
    return set.union(
        *[
            property_for_key_as_set(data, key)
            for key in ["to", "cc", "bto", "bcc", "audience"]
        ]
    )


def remove_public(recipients):
    return {
        x
        for x in recipients
        if x
        not in ["Public", "as:Public", "https://www.w3.org/ns/activitystreams#Public"]
    }


def is_public(data: dict) -> bool:
    """Determines if the object should be considered public based on its recipients"""
    recipients = recipients_for_object(data)

    return any(
        x in recipients
        for x in ["Public", "as:Public", "https://www.w3.org/ns/activitystreams#Public"]
    )


def fediverse_handle_from_actor(actor: dict) -> str:
    """Given an actor object, i.e. a dict, determines the fediverse handle"""
    host = urlparse(actor["id"]).netloc
    username = urlparse(actor["id"]).path.split("/")[-1]

    if "preferredUsername" in actor:
        username = actor["preferredUsername"]

    return f"{username}@{host}"


def copy_to_and_cc(origin: dict, destination: dict) -> dict:
    """Copies the audience from the origin object to the destination object"""

    for key in ["to", "cc", "bto", "bcc", "audience"]:
        if key in origin:
            destination[key] = list(
                property_for_key_as_set(origin, key)
                | property_for_key_as_set(destination, key)
            )

    return destination
