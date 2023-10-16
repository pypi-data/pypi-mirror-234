from unittest.mock import AsyncMock

from .event_source import EventSource


async def test_event_source() -> None:
    session = AsyncMock()
    content = AsyncMock()
    response = AsyncMock(content=content)
    session.get.return_value = response
    response.raise_for_status = lambda: 1

    event_source = EventSource(session, "url")

    content.__aiter__.return_value = [b"data: text\n", b"\n", b"\n", b"\n", b"\n"]
    event = await event_source.__anext__()
    assert event.data == "text"

    content.__aiter__.return_value = [b"\n", b"\n", b"data: text\n", b"\n"]
    event = await event_source.__anext__()
    assert event.data == "text"
