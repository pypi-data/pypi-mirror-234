import json
import logging
import re

import aiohttp

from .utils import BOVINE_CLIENT_NAME

logger = logging.getLogger(__name__)


async def lookup_with_webfinger(
    session: aiohttp.ClientSession, webfinger_url: str, params: dict
):
    async with session.get(
        webfinger_url, params=params, headers={"user-agent": BOVINE_CLIENT_NAME}
    ) as response:
        if response.status != 200:
            logger.warning(f"{params['resource']} not found using webfinger")
            return None
        text = await response.text()
        data = json.loads(text)

        if "links" not in data:
            return None

        links = data["links"]
        for entry in links:
            if "rel" in entry and entry["rel"] == "self":
                if re.match(r"application/.*json", entry["type"]):
                    return entry["href"]

    return None
