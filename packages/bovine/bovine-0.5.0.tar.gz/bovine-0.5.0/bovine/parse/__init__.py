from bovine.clients import lookup_uri_with_webfinger

from .bovine_object import BovineObject


class Actor(BovineObject):
    """Parses an actor object"""

    def __init__(self, data, domain: str = None, domain_may_differ: bool = False):
        super().__init__(data, domain=domain, domain_may_differ=domain_may_differ)

        if "outbox" not in self.data:
            raise ValueError("An actor must have an outbox")
        if not isinstance(self.data["outbox"], str):
            raise ValueError("The outbox must be a single string")
        if "inbox" not in self.data:
            raise ValueError("An actor must have an inbox")
        if not isinstance(self.data["inbox"], str):
            raise ValueError("The inbox must be a single string")
        self.webfinger_identifier = None

    @property
    def id(self):
        """id of the actor"""
        return self.data.get("id")

    @property
    def unvalidated_acct_uri(self) -> str | None:
        username = self.data.get("preferredUsername")
        if isinstance(username, dict):
            username = username.get("@value")
        if not isinstance(username, str):
            return None
        if len(username) == 0:
            return None
        return f"acct:{username}@{self.domain}"

    def publicKeyPem(self, key_id):
        key = self.data.get("publicKey", {})
        if key.get("owner") != self.id:
            raise Exception("Key has incorrect owner")
        return key.get("publicKeyPem")

    @property
    def identifiers(self):
        """Lists the identifiers of the actor.

        In order for the account uri to be listed as an identifier,
        the coroutine validate_acct_uri needs to be run"""
        result = set()
        if self.id:
            result.add(self.id)
        if self.webfinger_identifier:
            result.add(self.webfinger_identifier)
        return result

    async def validate_acct_uri(self, session=None) -> bool:
        """Checks if the acct uri defined by preferredUsername and
        the domain can be verified using a webfinger lookup.
        If yes, returns True and adds the acct uri to the
        identifiers of the actor."""
        lookup_id, _ = await lookup_uri_with_webfinger(
            session, self.unvalidated_acct_uri
        )

        if lookup_id == self.id:
            self.webfinger_identifier = self.unvalidated_acct_uri
            return True

        return False


class Activity(BovineObject):
    """Represents an activity"""

    @property
    def is_accept(self) -> bool:
        return self.data.get("type") == "Accept"

    @property
    def is_create(self) -> bool:
        return self.data.get("type") == "Create"

    @property
    def is_follow(self) -> bool:
        return self.data.get("type") == "Follow"

    @property
    def is_undo(self) -> bool:
        return self.data.get("type") == "Undo"

    async def object_for_create(self, retrieve) -> dict | None:
        """If activity is a create, returns the corresponding object"""
        if not self.is_create:
            return

        obj = self.data.get("object")
        if obj is None:
            return

        if isinstance(obj, str):
            obj = await retrieve(obj)
        if not isinstance(obj, dict):
            return
        obj = Object(obj, domain=self.domain)

        if (
            obj.attributed_to_id
            and self.actor_id
            and self.actor_id != obj.attributed_to_id
        ):
            raise ValueError("actor_id and attributed_to must match")

        return obj

    async def accept_for_follow(self, retrieve) -> dict | None:
        """If the activity is an Accept for a Follow request, returns said
        Follow request. Basic validation is run on the Accept and Follow
        request.

        In case of not an Accept for a Follow request or it being invalid
        None is returned.

        :param retrieve: a coroutine str -> dict that takes an object_id and
            resolves it to the corresponding object

        :param retrieve: a coroutine str -> dict that takes an object_id and
            resolves it to the corresponding object"""

        if not self.is_accept:
            return None
        follow = self.data.get("object")
        if not follow:
            return None
        if isinstance(follow, str):
            follow = await retrieve(follow)
        if not isinstance(follow, dict):
            return None

        follow = Activity(follow, domain=self.domain, domain_may_differ=True)

        if not follow.is_follow:
            return None

        if follow.object_id != self.actor_id:
            return None

        return follow

    async def undo_of_follow(self, retrieve) -> dict | None:
        """If the activity is an Undo of a Follow request, returns said
        Follow request. Basic validation is run on the Undo and Follow
        request.

        In case of not an Undo of a Follow request or it being invalid
        None is returned.

        :param retrieve: a coroutine str -> dict that takes an object_id and
            resolves it to the corresponding object"""

        if not self.is_undo:
            return None

        follow = self.data.get("object")
        if not follow:
            return None
        if isinstance(follow, str):
            follow = await retrieve(follow)
        if not isinstance(follow, dict):
            return None
        follow = Activity(follow, domain=self.domain, domain_may_differ=True)
        if not follow.is_follow:
            return None

        if follow.domain != self.domain:
            return None
        if follow.actor_id and self.actor_id and follow.actor_id != self.actor_id:
            return None

        return follow


class Object(BovineObject):
    """Basic representation of an object"""

    @property
    def attributed_to_id(self):
        attributed_to = self.data.get("attributedTo")
        if isinstance(attributed_to, dict):
            attributed_to = attributed_to.get("id")
        return attributed_to

    @property
    def in_reply_to(self):
        return self.data.get("inReplyTo")

    @property
    def identifier(self):
        return self.data.get("id")

    @property
    def mentions(self):
        return [x for x in self.tags if x.get("type") == "Mention"]

    @property
    def tags(self):
        tags = self.data.get("tag", [])
        if isinstance(tags, list):
            return tags
        return [tags]
