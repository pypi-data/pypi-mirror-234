import logging
import os
import traceback
from typing import Optional, Tuple

import aiodns
import aiohttp

from bovine.utils import parse_fediverse_handle

from .lookup_account import lookup_with_webfinger
from .nodeinfo import fetch_nodeinfo20, fetch_nodeinfo_document

logger = logging.getLogger(__name__)


async def lookup_account_with_webfinger(
    session: aiohttp.ClientSession, fediverse_handle: str
) -> str | None:
    """**Deprecated**: Use lookup_uri_with_webfinger instead

    Looks up the actor url associated with a FediVerse handle,
    i.e. an identifier of the form username@domain, using
    the webfinger endpoint

    :param session: the aiohttp.ClientSession to use
    :param fediverse_handle: the FediVerse handle as a string
    """
    result, _ = await lookup_uri_with_webfinger(session, "acct:" + fediverse_handle)
    return result


async def lookup_did_with_webfinger(
    session: aiohttp.ClientSession, domain: str, did: str
):
    """**Deprecated**: Use lookup_uri_with_webfinger instead

    Looks up the actor url associated with a did and domain
    using the webfinger endpoint

    :param session: the aiohttp.ClientSession to use
    :param domain: the domain to perform the lookup from
    :param did: the did key to perform lookup with
    """
    result, _ = await lookup_uri_with_webfinger(session, did, domain=domain)
    return result


async def lookup_uri_with_webfinger(
    session: aiohttp.ClientSession, uri: str, domain: str | None = None
) -> Tuple[Optional[str], Optional[bool]]:
    """Looks up an actor URI associated with an URI and domain
    using the webfinger endpoint following `fep-4adb
    <https://codeberg.org/fediverse/fep/src/branch/main/feps/fep-4adb.md>`_

    :param session: the aiohttp.ClientSession to use
    :param uri: the uri to perform lookup with
    :param domain: the domain to perform the lookup from
    :returns: A tuple of `(actor URI, verification_necessary)`. The value
        of `verification_necessary` indicates that it is necessary if the actor
        has the appropriate authority to associate the query URI with itself.

    """
    if domain is None:
        if uri.startswith("acct:"):
            _, domain = parse_fediverse_handle(uri.removeprefix("acct:"))
        else:
            raise ValueError(f"For the uri {uri} a domain must be specified")

    if domain.startswith("http://") or domain.startswith("https://"):
        webfinger_url = f"{domain}/.well-known/webfinger"
    else:
        webfinger_url = f"https://{domain}/.well-known/webfinger"
    params = {"resource": uri}

    try:
        result = await lookup_with_webfinger(session, webfinger_url, params)
    except aiohttp.client_exceptions.ClientConnectorError as ex:
        if os.environ.get("BUTCHER_ALLOW_HTTP"):
            webfinger_url = webfinger_url.replace("https://", "http://")
            result = await lookup_with_webfinger(session, webfinger_url, params)
        else:
            raise ex
    return result, not uri.startswith("acct:")


async def lookup_with_dns(session: aiohttp.ClientSession, domain: str) -> str | None:
    """Looks up the actor url associated with the dns entry for domain. See
    `FEP-612d: Identifying ActivityPub Objects through DNS
    <https://codeberg.org/fediverse/fep/src/branch/main/feps/fep-612d.md>`_ for
    the mechanism.

    :param session: the aiohttp.ClientSession to use
    :param domain: the domain to perform the lookup from
    """

    resolver = aiodns.DNSResolver()
    try:
        (result,) = await resolver.query(f"_apobjid.{domain}", "TXT")

        return result.text
    except Exception:
        return None


async def fetch_nodeinfo(session: aiohttp.ClientSession, domain: str) -> dict | None:
    """Fetches the nodeinfo 2.0 object from domain using the /.well-known/nodeinfo
    endpoint"""

    try:
        data = await fetch_nodeinfo_document(session, domain)

        for link in data["links"]:
            if link["rel"] == "http://nodeinfo.diaspora.software/ns/schema/2.0":
                return await fetch_nodeinfo20(session, link["href"])

        return None

    except Exception as e:
        logger.error(str(e))
        for log_line in traceback.format_exc().splitlines():
            logger.error(log_line)
        return None
