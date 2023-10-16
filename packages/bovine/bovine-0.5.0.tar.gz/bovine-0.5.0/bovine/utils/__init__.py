from datetime import datetime, timezone
from typing import Optional, Tuple

from bs4 import BeautifulSoup


def webfinger_response_json(account: str, url: str) -> dict:
    """helper to generate a webfinger response"""
    return {
        "subject": account,
        "links": [
            {
                "href": url,
                "rel": "self",
                "type": "application/activity+json",
            }
        ],
    }


def parse_fediverse_handle(account: str) -> Tuple[str, Optional[str]]:
    """Splits fediverse handle in name and domain"""
    if account[0] == "@":
        account = account[1:]

    if "@" in account:
        return tuple(account.split("@", 1))
    return account, None


def now_isoformat() -> str:
    """Returns now in Isoformat, e.g. "2023-05-31T18:11:35Z", to be used as the value
    of published"""
    return (
        datetime.now(tz=timezone.utc).replace(microsecond=0, tzinfo=None).isoformat()
        + "Z"
    )


def activity_pub_object_id_from_html_body(body: str) -> str | None:
    """Determines the object identifier from the html body
    by parsing it and looking for link tags with rel="alternate"
    and type application/activity+json"""

    soup = BeautifulSoup(body, features="lxml")
    element = soup.find(
        "link", attrs={"rel": "alternate", "type": "application/activity+json"}
    )
    if not element:
        return None

    return element.attrs.get("href")
