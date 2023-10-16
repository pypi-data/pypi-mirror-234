from dataclasses import dataclass, field
from typing import List, Optional, Set

from bovine.utils import now_isoformat

from .utils import fediverse_handle_from_actor


@dataclass
class Object:
    """A dataclass representing an `ActivityStreams Object
    <https://www.w3.org/TR/activitystreams-vocabulary/#object-types>`_"""

    type: str
    attributed_to: Optional[str] = None
    followers: Optional[str] = None
    id: Optional[str] = None
    published: Optional[str] = None
    to: Set[str] = field(default_factory=set)
    cc: Set[str] = field(default_factory=set)

    name: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    source: Optional[dict] = None

    width: Optional[int] = None
    height: Optional[int] = None

    in_reply_to: Optional[str] = None
    url: Optional[str] = None
    tag: List[dict] = field(default_factory=list)
    attachment: List[dict] = field(default_factory=list)
    href: Optional[str] = None

    def as_public(self):
        """makes the object public, i.e. public in to and followers in cc"""
        self.to.add("https://www.w3.org/ns/activitystreams#Public")
        if self.followers:
            self.cc.add(self.followers)
        return self

    def as_followers(self):
        """addresses the object to followers, if they are set"""
        if self.followers:
            self.to.add(self.followers)
        return self

    def as_unlisted(self):
        """makes the object unlisted, i.e. public in cc and followers in to"""
        if self.followers:
            self.to.add(self.followers)
        self.cc.add("https://www.w3.org/ns/activitystreams#Public")
        return self

    def now(self):
        """Sets published to now in isoformat"""
        self.published = now_isoformat()
        return self

    def build(self):
        """Returns the resulting object as a dictionary"""
        result = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": self.type,
        }

        extra_fields = {
            "attributedTo": self.attributed_to,
            "to": list(self.to),
            "cc": list(self.cc - self.to),
            "id": self.id,
            "inReplyTo": self.in_reply_to,
            "published": self.published,
            "source": self.source,
            "name": self.name,
            "url": self.url,
            "summary": self.summary,
            "content": self.content,
            "tag": self.tag,
            "attachment": self.attachment,
            "href": self.href,
            "width": self.width,
            "height": self.height,
        }

        for key, value in extra_fields.items():
            if value:
                result[key] = value

        if "to" in result and len(result["to"]) == 0:
            del result["to"]
        if "cc" in result and len(result["cc"]) == 0:
            del result["cc"]

        return result


class ObjectFactory:
    """ObjectFactory usually created through a BovineClient"""

    def __init__(self, actor_information=None, client=None):
        if client:
            self.client = client
            self.information = client.information
        elif actor_information:
            self.client = None
            self.information = actor_information
        else:
            raise TypeError(
                "You need to either specify actor_information or a BovineClient"
            )

    def note(self, **kwargs):
        """Creates a Note Object"""
        return Object(
            attributed_to=self.information["id"],
            type="Note",
            followers=self.information.get("followers"),
            **kwargs
        )

    def reply(self, obj, **kwargs):
        """Creates a reply for an object"""
        cc = (set(obj.get("to", [])) | set(obj.get("cc", []))) - {
            self.information["id"]
        }
        return Object(
            attributed_to=self.information["id"],
            type=obj.get("type", "Note"),
            in_reply_to=obj.get("id"),
            followers=self.information.get("followers"),
            to={obj.get("attributedTo")},
            cc=cc,
            **kwargs
        )

    def article(self, **kwargs):
        """Creates an Article Object"""
        return Object(
            attributed_to=self.information["id"],
            type="Article",
            followers=self.information.get("followers"),
            **kwargs
        )

    def event(self, **kwargs):
        """Creates an Event Object"""
        return Object(
            attributed_to=self.information["id"],
            type="Event",
            followers=self.information.get("followers"),
            **kwargs
        )

    async def mention_for_actor_uri(self, actor_to_mention):
        """Creates a mention object for another actor. Requires client to be set.

        :param actor_to_mention: The URI of the actor to mention"""

        if not self.client:
            raise TypeError("client needs to be set at construction")

        remote_actor = await self.client.proxy(actor_to_mention)

        return Object(
            type="Mention",
            href=actor_to_mention,
            name=fediverse_handle_from_actor(remote_actor),
        )
