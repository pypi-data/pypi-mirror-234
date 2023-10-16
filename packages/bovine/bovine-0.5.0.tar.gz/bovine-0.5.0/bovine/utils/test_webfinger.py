import re

from . import now_isoformat, webfinger_response_json


def test_webfinger():
    response = webfinger_response_json("acct:name@domain", "url")

    assert "subject" in response
    assert "links" in response


def test_now_isoformat():
    result = now_isoformat()
    assert re.match(
        r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$",
        result,
    )
