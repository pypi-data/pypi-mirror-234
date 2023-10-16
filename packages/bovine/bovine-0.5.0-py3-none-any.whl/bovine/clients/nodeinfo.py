import json
import logging
import traceback

import aiohttp

from .utils import BOVINE_CLIENT_NAME

logger = logging.getLogger(__name__)


async def fetch_nodeinfo_document(session: aiohttp.ClientSession, domain: str) -> dict:
    wellknown_nodeinfo_url = f"https://{domain}/.well-known/nodeinfo"

    async with session.get(
        wellknown_nodeinfo_url,
        headers={"user-agent": BOVINE_CLIENT_NAME},
        timeout=60,
    ) as response:
        return await response.json()


async def fetch_nodeinfo20(session: aiohttp.ClientSession, url: str) -> dict | None:
    try:
        async with session.get(
            url, headers={"user-agent": BOVINE_CLIENT_NAME}
        ) as response:
            text = await response.text()
            return json.loads(text)

    except Exception as e:
        logger.error(str(e))
        for log_line in traceback.format_exc().splitlines():
            logger.error(log_line)
        return None
