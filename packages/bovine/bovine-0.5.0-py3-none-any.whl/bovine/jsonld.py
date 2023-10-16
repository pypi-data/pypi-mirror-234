import json
import logging
from typing import List

import requests_cache
from pyld import jsonld

from bovine.utils.pyld_requests import requests_document_loader

requests_cache.install_cache("context_cache")

logger = logging.getLogger(__name__)


default_context = [
    "https://www.w3.org/ns/activitystreams",
    "https://w3id.org/security/v1",
    {
        "Hashtag": "as:Hashtag",
    },
]
"""Defines the context used to communicate with other Fediverse software"""


bovine_context = [
    "https://www.w3.org/ns/activitystreams",
    {
        "publicKey": {"@id": "https://w3id.org/security#publicKey", "@type": "@id"},
        "publicKeyPem": "https://w3id.org/security#publicKeyPem",
        "owner": {"@id": "https://w3id.org/security#owner", "@type": "@id"},
        "to": {"@id": "as:to", "@type": "@id", "@container": "@set"},
        "cc": {"@id": "as:cc", "@type": "@id", "@container": "@set"},
        "tag": {"@id": "as:tag", "@type": "@id", "@container": "@set"},
        "items": {"@id": "as:items", "@type": "@id", "@container": "@set"},
        "attachment": {"@id": "as:attachment", "@type": "@id", "@container": "@set"},
        "Hashtag": "as:Hashtag",
    },
]
""" Defines the context about:bovine used internally in the bovine stack"""

bovine_context_name = "about:bovine"
"""Defines the name of the bovine context"""


def wrapper(url, options, **kwargs):
    if url == bovine_context_name:
        return {
            "contentType": "application/ld+json",
            "contextUrl": None,
            "documentUrl": url,
            "document": {"@context": bovine_context},
        }
    elif url.startswith("http://joinmastodon.org/ns") or url.startswith(
        "http://schema.org"
    ):
        # See https://github.com/go-fed/activity/issues/152 for why
        return {
            "contentType": "application/ld+json",
            "contextUrl": None,
            "documentUrl": url,
            "document": {"@context": {}},
        }
    result = requests_document_loader(timeout=60)(url, options)
    return result


jsonld.set_document_loader(wrapper)


async def split_into_objects(input_data: dict) -> List[dict]:
    """Takes an object with an "id" property and separates
    out all the subobjects with an id"""

    if "@context" not in input_data:
        logger.warning("@context missing in %s", json.dumps(input_data))
        input_data["@context"] = default_context

    context = input_data["@context"]
    flattened = jsonld.flatten(input_data)
    compacted = jsonld.compact(flattened, context)

    if "@graph" not in compacted:
        return [compacted]

    local, remote = split_remote_local(compacted["@graph"])

    return [frame_object(obj, local, context) for obj in remote]


def frame_object(obj: dict, local: List[dict], context) -> dict:
    to_frame = {"@context": context, "@graph": [obj] + local}
    frame = {"@context": context, "id": obj["id"]}
    return jsonld.frame(to_frame, frame)


def split_remote_local(graph):
    local = [x for x in graph if x["id"].startswith("_")]
    remote = [x for x in graph if not x["id"].startswith("_")]

    return local, remote


def combine_items(data: dict, items: List[dict]) -> dict:
    """Takes data and replaces ids by the corresponding objects from items"""
    return frame_object(data, items, data["@context"])


def with_bovine_context(data: dict) -> dict:
    """Returns the object with the about:bovine context"""
    return use_context(data, "about:bovine")


def with_external_context(data: dict) -> dict:
    """Returns the object with the default external context"""
    return use_context(data, default_context)


def use_context(data, context):
    return jsonld.compact(data, context)


def value_from_object(data, key):
    result = data.get(key)
    if result is None:
        return result
    if isinstance(result, str):
        return result
    return result["@value"]
