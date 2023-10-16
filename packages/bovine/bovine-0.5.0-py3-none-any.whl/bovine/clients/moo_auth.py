from bovine.crypto.helper import content_digest_sha256
from bovine.crypto.http_signature import build_signature
from bovine.utils.date import get_gmt_now

from .event_source import EventSource
from .utils import BOVINE_CLIENT_NAME, host_target_from_url


class MooAuthClient:
    """Client for using Moo-Auth-1 authentication"""

    def __init__(self, session, did_key, private_key):
        self.session = session
        self.did_key = did_key
        self.private_key = private_key

    async def get(self, url, headers={}):
        host, target = host_target_from_url(url)

        accept = "application/activity+json"
        date_header = get_gmt_now()

        signature_helper = build_signature(host, "get", target).with_field(
            "date", date_header
        )
        signature_header = signature_helper.ed25519_sign(self.private_key)

        headers = {
            "accept": accept,
            "user-agent": BOVINE_CLIENT_NAME,
            **headers,
            **signature_helper.headers,
            "authorization": f"Moo-Auth-1 {self.did_key}",
            "x-moo-signature": signature_header,
        }

        return await self.session.get(url, headers=headers)

    async def post(self, url, body, headers={}, content_type=None):
        host, target = host_target_from_url(url)
        accept = "application/activity+json"
        # LABEL: ap-s2s-content-type
        if content_type is None:
            content_type = "application/activity+json"
        date_header = get_gmt_now()

        digest = content_digest_sha256(body)

        signature_helper = (
            build_signature(host, "post", target)
            .with_field("date", date_header)
            .with_field("digest", digest)
        )
        signature_header = signature_helper.ed25519_sign(self.private_key)

        headers = {
            "accept": accept,
            "content-type": content_type,
            "user-agent": BOVINE_CLIENT_NAME,
            **headers,
            **signature_helper.headers,
            "authorization": f"Moo-Auth-1 {self.did_key}",
            "x-moo-signature": signature_header,
        }

        return await self.session.post(url, data=body, headers=headers)

    def event_source(self, url, headers={}):
        host, target = host_target_from_url(url)
        date_header = get_gmt_now()
        accept = "text/event-stream"
        signature_helper = build_signature(host, "get", target).with_field(
            "date", date_header
        )
        signature_header = signature_helper.ed25519_sign(self.private_key)

        headers = {
            "accept": accept,
            "user-agent": BOVINE_CLIENT_NAME,
            **headers,
            **signature_helper.headers,
            "authorization": f"Moo-Auth-1 {self.did_key}",
            "x-moo-signature": signature_header,
        }

        return EventSource(self.session, url, headers=headers)
