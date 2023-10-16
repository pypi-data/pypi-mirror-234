import aiohttp

from bovine.utils.date import get_gmt_now

from .event_source import EventSource
from .utils import BOVINE_CLIENT_NAME


class BearerAuthClient:
    """Client for using Bearer authentication"""

    def __init__(self, session: aiohttp.ClientSession, bearer_key: str):
        self.session = session
        self.bearer_key = bearer_key

    async def get(self, url: str, headers: dict = {}):
        accept = "application/activity+json"
        date_header = get_gmt_now()

        headers["accept"] = accept
        headers["date"] = date_header
        headers["authorization"] = f"Bearer {self.bearer_key}"
        headers["user-agent"] = BOVINE_CLIENT_NAME

        return await self.session.get(url, headers=headers)

    async def post(
        self, url: str, body: str, headers: dict = {}, content_type: str | None = None
    ):
        accept = "application/activity+json"
        # LABEL: ap-s2s-content-type
        if content_type is None:
            content_type = "application/activity+json"
        date_header = get_gmt_now()

        headers["accept"] = accept
        headers["content-type"] = content_type
        headers["date"] = date_header
        headers["authorization"] = f"Bearer {self.bearer_key}"

        return await self.session.post(url, data=body, headers=headers)

    def event_source(self, url: str, headers: dict = {}) -> EventSource:
        """Returns an EventSource for the server sent events given by url"""

        date_header = get_gmt_now()
        accept = "text/event-stream"

        headers["accept"] = accept
        headers["date"] = date_header
        headers["authorization"] = f"Bearer {self.bearer_key}"
        headers["user-agent"] = BOVINE_CLIENT_NAME

        return EventSource(self.session, url, headers=headers)
