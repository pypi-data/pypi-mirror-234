import json
import logging
from typing import Optional
from urllib.parse import urlencode, urlparse

import tomllib

from .activitystreams import Collection
from .activitystreams.activity_factory import ActivityFactory
from .activitystreams.collection_helper import CollectionHelper
from .activitystreams.object_factory import ObjectFactory
from .clients.authorization_wrapper import AuthorizationWrapper
from .utils import activity_pub_object_id_from_html_body

logger = logging.getLogger(__name__)


class BovineClient(AuthorizationWrapper):
    """BovineClient is meant to serve as the basis of building ActivityPub Clients.
    It defines methods for interacting with the endpoints defined by the corresponding
    ActivityPub Actor: inbox, outbox, and proxyUrl.

    Usage is either:

    .. code-block:: python

        async with BovineClient(**config) as actor:
            await do_something(actor)

    or

    .. code-block:: python

        actor = await BovineClient(**config)
        await actor.init()
        await do_something(actor)

    I still call the variable actor as it represents the ActivityPub Actor through
    a client.

    :param domain: Specifies the domain the actor is on, used for Moo-Auth-1
    :param host: Alias for domain
    :param actor_id: URI of the actor, used for Bearer Auth and HTTP Signatures
    :param account_url: Alias for actor_id
    :param secret: The private key material for Moo-Auth-1 and HTTP Signatures
    :param access_token: The access token for Bearer auth
    """

    def __init__(self, **kwargs):
        super().__init__(
            domain=kwargs.get("domain", kwargs.get("host")),
            secret=kwargs.get("secret"),
            actor_id=kwargs.get("actor_id", kwargs.get("account_url")),
            public_key_url=kwargs.get("public_key_url"),
            access_token=kwargs.get("access_token"),
        )

        self.information: Optional[dict] = None
        self._activity_factory = None
        self._object_factory = None

    async def get(self, target):
        assert self.client

        response = await self.client.get(target)
        response.raise_for_status()
        return json.loads(await response.text())

    async def init(self, session=None):
        """Manually initializes the BovineClient for cases when
        not used within async with. Also loads the actor information.

        :param session:
            can be used to specify an existing aiohttp.ClientSession. Otherwise a new
            one is created.
        """

        await super().init(session=session)

        if self.client is None:
            raise Exception("Client not set in BovineClient")
        self.information = await self.get(self.actor_id)

        logger.debug("Retrieved information %s", self.information)

        if any(required not in self.information for required in ["inbox", "outbox"]):
            raise Exception("Retrieved incomplete actor data")

    async def send_to_outbox(self, data: dict):
        """sends data to outbox of actor

        :param data: The data to send as python dict

        :return:
            The aiohttp.ClientResponse object. This means
            return_value.headers["location"] will contain the id of the
            posted activity.
        """
        if self.information is None:
            await self.init()

        assert self.client

        return await self.client.post(self.information["outbox"], json.dumps(data))

    async def proxy(self, target: str):
        """Retrieve's an element through the actors' proxyUrl endpoint
        as specified in ActivityPub.

            :param target: The URL of the object to retrieve


        FIXME: Support for non-json stuff"""
        response = await self.client.post(
            self.information["endpoints"]["proxyUrl"],
            urlencode({"id": target}),
            content_type="application/x-www-form-urlencoded",
        )
        response.raise_for_status()
        return await response.json()

    async def event_source(self):
        """Returns an EventSource corresponding to the actor's

        The syntax for this will probably change"""
        if self.information is None:
            await self.load()

        event_source_url = self.information["endpoints"]["eventSource"]
        return self.client.event_source(event_source_url)

    async def simplify_collection(self, collection):
        """Returns a Collection containing all items from the passed collection
        or collection id"""
        # items = await all_collection_elements(self, collection)

        items = []

        if isinstance(collection, str):
            collection_id = collection
        else:
            collection_id = collection.get("id")
        return Collection(id=collection_id, items=items).build()

    @property
    def activity_factory(self):
        """Returns an ActivityFactory for objects corresponding to the client's actor"""
        if self._activity_factory is None:
            self._activity_factory = ActivityFactory(self.information)
        return self._activity_factory

    @property
    def object_factory(self):
        """Returns an ObjectFactory for objects corresponding to the client's actor"""
        if self._object_factory is None:
            self._object_factory = ObjectFactory(client=self)
        return self._object_factory

    @property
    def factories(self):
        return self.activity_factory, self.object_factory

    @property
    def host(self):
        """The host the actor is on"""
        return urlparse(self.actor_id).netloc

    @property
    def followers(self) -> str:
        """The id of the follows collection"""
        return self.information["followers"]

    def inbox(self, resolve=True):
        """Provides a CollectionHelper for the Actors inbox"""
        inbox_collection = CollectionHelper(
            self.information["inbox"], self, resolve=resolve
        )
        return inbox_collection

    def outbox(self, resolve=True):
        """Provides a CollectionHelper for the Actors outbox"""
        inbox_collection = CollectionHelper(
            self.information["outbox"], self, resolve=resolve
        )
        return inbox_collection

    def collection_helper(self, collection, resolve=False):
        """Returns a CollectionHelper for the collection provided. Usage:

        .. code-block:: python

            async for x in client.collection_helper(uri_of_collection):
                await do_something(x)

        :param collection: Uri of the collection to irater over
        :param resolve: If true objects are automatically fetched"""

        return CollectionHelper(collection, self, resolve=resolve)

    @staticmethod
    def from_file(config_file: str):
        """Initializes the BovineClient from a toml config file"""
        with open(config_file, "rb") as fp:
            config = tomllib.load(fp)

        return BovineClient(**config)


class BovineActor(AuthorizationWrapper):
    r"""Defines the Bovine version of an ActivityPub Actor. This class is meant
    to be used when implementing an ActivityPub Server in order to handle the
    HTTP requests to another server.

    Currently most of these interactions use HTTP Signatures.

    Usage is either:

    .. code-block:: python

        async with BovineActor(**config) as actor:
            await do_something(actor)

    or

    .. code-block:: python

        actor = await BovineActor(**config)
        await actor.init()
        await do_something(actor)

    :param domain: Specifies the domain the actor is on, used for Moo-Auth-1
    :param host: Alias for domain
    :param actor_id: URI of the actor, used for Bearer Auth and HTTP Signatures
    :param account_url: Alias for actor_id
    :param secret: The private key material for Moo-Auth-1 and HTTP Signatures
    :param access_token: The access token for Bearer auth
    """

    def __init__(self, **config):
        super().__init__(
            domain=config.get("domain", config.get("host")),
            secret=config.get("secret"),
            actor_id=config.get("actor_id", config.get("acccount_url")),
            public_key_url=config.get("public_key_url"),
            access_token=config.get("access_token"),
        )

    async def init(self, session=None):
        """Manually initializes the BovineActor for cases when not used
        within async with

        :param session:
            can be used to specify an existing aiohttp.ClientSession. Otherwise a new
            one is created.
        """

        await super().init(session=session)

    async def post(self, target: str, data: dict):
        """Send a signed post with data to target"""
        response = await self.client.post(target, json.dumps(data))
        response.raise_for_status()

        return response

    async def get(self, target: str, fail_silently: bool = False):
        """Retrieve target with a get. An exception is raised if the request fails

        :param target: The URL of the object to retrieve
        :param fail_silently: do not raise an exception if the request fails
        """
        response = await self.client.get(target)
        if fail_silently and response.status >= 400:
            return None

        if response.status >= 300 and response.status < 400:
            if "Location" in response.headers:
                return await self.get(response.headers["Location"])
            return None

        if response.status in [404, 410]:
            body = await response.text()
            try:
                result = json.loads(body)
                if result["type"] == "Tombstone":
                    return result
            except Exception:
                ...

        response.raise_for_status()

        body = await response.text()

        try:
            return json.loads(body)
        except Exception:
            # if "json" not in response.headers.get("Content-Type"):
            if "alternate" in response.links:
                link_header = response.links["alternate"]
                if "json" in link_header["type"]:
                    return await self.get(
                        str(link_header["url"]), fail_silently=fail_silently
                    )

            object_id = activity_pub_object_id_from_html_body(body)

            if object_id:
                return await self.get(object_id, fail_silently=fail_silently)
            else:
                return None

    async def get_ordered_collection(self, url: str, max_items: Optional[int] = None):
        """Retrieve target ordered collection

        :param url: url of the ordered collection
        :param max_items: maximal number of items to retrieve, use None for all
        """
        result = await self.client.get(url)
        result.raise_for_status()

        data = json.loads(await result.text())

        total_number_of_items = data["totalItems"]
        items = []

        if "orderedItems" in data:
            items = data["orderedItems"]

        if len(items) == total_number_of_items:
            return {"total_items": total_number_of_items, "items": items}

        if "first" in data:
            page_data = await self.get(data["first"])

            items = page_data["orderedItems"]

            while "next" in page_data and len(page_data["orderedItems"]) > 0:
                if max_items and len(items) > max_items:
                    return {"total_items": total_number_of_items, "items": items}

                page_data = await self.get(page_data["next"])

                items += page_data["orderedItems"]

        return {"total_items": total_number_of_items, "items": items}

    @staticmethod
    def from_file(config_file: str):
        with open(config_file, "rb") as fp:
            config = tomllib.load(fp)

        return BovineActor(**config)
