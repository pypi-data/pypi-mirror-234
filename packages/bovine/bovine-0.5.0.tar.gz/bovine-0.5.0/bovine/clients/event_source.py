from typing import Dict

import aiohttp

from bovine.types import ServerSentEvent


class EventSource:
    def __init__(
        self, session: aiohttp.ClientSession, url: str, headers: Dict[str, str] = {}
    ):
        self.session = session
        self.url: str = url
        self.headers = headers
        self.response: aiohttp.ClientResponse | None = None

    async def create_response(self) -> None:
        timeout = aiohttp.ClientTimeout(total=None)

        self.response = await self.session.get(
            self.url,
            headers={"Accept": "text/event-stream", **self.headers},
            timeout=timeout,
            allow_redirects=False,
        )
        assert self.response
        self.response.raise_for_status()

        if self.response.status == 301:
            self.url = self.response.headers["location"]
            await self.create_response()

    def __aiter__(self):
        return self

    async def __anext__(self) -> ServerSentEvent | None:
        if self.response is None:
            await self.create_response()

        to_parse = ""

        assert self.response

        async for line_in_bytes in self.response.content:
            line = line_in_bytes.decode("utf-8")
            if line[0] == ":":
                continue
            if line == "\n":
                event = ServerSentEvent.parse_utf8(to_parse)
                if event.data:
                    return event
            else:
                to_parse = f"{to_parse}{line}"

        return None
