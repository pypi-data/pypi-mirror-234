import logging
from typing import Optional
from dataclasses import dataclass

import aiohttp

from bovine.crypto import private_key_to_did_key

from . import lookup_did_with_webfinger
from .bearer import BearerAuthClient
from .moo_auth import MooAuthClient
from .signed_http import SignedHttpClient

logger = logging.getLogger(__name__)


@dataclass
class AuthorizationWrapper:
    actor_id: str | None = (None,)
    public_key_url: str | None = (None,)
    access_token: str | None = (None,)
    secret: str | None = (None,)
    domain: str | None = (None,)
    client: BearerAuthClient | MooAuthClient | SignedHttpClient = None
    session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, *args):
        await self.session.close()

    async def init(self, session: Optional[aiohttp.ClientSession] = None):
        self.session = session
        if session is None:
            self.session = aiohttp.ClientSession()

        if self._has_moo_auth():
            await self.with_host_and_ed25519_private_key(
                self.domain, self.secret, session=self.session
            )
        elif self._has_http_signature():
            self.actor_id = self.actor_id
            self.with_http_signature(
                self.public_key_url,
                self.secret,
                session=self.session,
            )
        elif self._has_bearer_auth():
            self.actor_id = self.actor_id
            self.with_bearer_token(self.access_token, session=self.session)
        else:
            raise Exception("No known authorization method available")

    async def with_host_and_ed25519_private_key(
        self,
        host: str,
        private_key: str,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        if session is None:
            session = aiohttp.ClientSession()
        did_key = private_key_to_did_key(private_key)

        self.actor_id = await lookup_did_with_webfinger(session, host, did_key)

        if not isinstance(self.actor_id, str):
            logger.error("Failed to lookup actor id")
            raise Exception("Failed to create Moo Auth Client")

        self.client = MooAuthClient(session, did_key, private_key)

        return self

    def with_actor_id(self, actor_id: str):
        self.actor_id = actor_id
        return self

    def with_http_signature(
        self,
        public_key_url: str,
        private_key: str,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        if session is None:
            session = aiohttp.ClientSession()

        self.client = SignedHttpClient(session, public_key_url, private_key)

        return self

    def with_bearer_token(
        self,
        access_token: str,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        if session is None:
            session = aiohttp.ClientSession()

        self.client = BearerAuthClient(session, access_token)

        return self

    def _has_http_signature(self):
        return self.actor_id and self.public_key_url and self.secret

    def _has_moo_auth(self):
        return self.domain and self.secret

    def _has_bearer_auth(self):
        return self.actor_id and self.access_token
