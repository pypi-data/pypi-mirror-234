from urllib.parse import urlparse


def netloc(identifier: str | None) -> str | None:
    if identifier is None:
        return None
    if identifier.startswith("http://") or identifier.startswith("https"):
        return urlparse(identifier).netloc
    return None


class BovineObject:
    """Initializes an Object to be parsed

    :param data: The data to be parsed. It is assumed that data is
        compacted against the **about:bovine** context and the parts
        making it up are validated."""

    def __init__(self, data: dict, domain: str = None, domain_may_differ: bool = False):
        if data.get("@context", "about:bovine") != "about:bovine":
            raise ValueError("@context must be 'about:bovine'")
        self.data = {"@context": "about:bovine", **data}

        if domain:
            id_domain = netloc(data.get("id"))
            if domain_may_differ:
                if id_domain:
                    self.domain = id_domain
                else:
                    self.domain = domain
            else:
                if id_domain and domain != id_domain:
                    raise ValueError("Domain and netloc of id must match")
                self.domain = domain
        else:
            if data.get("id") is None:
                raise ValueError(
                    "Either domain needs to be specified or data needs to have an id"
                )
            self.domain = urlparse(data.get("id")).netloc

    @property
    def actor_id(self):
        """If the object has an actor property, set to its id"""
        result = self.data.get("actor")
        if isinstance(result, dict):
            result = result.get("id")
        if netloc(result) and netloc(result) != self.domain:
            raise ValueError("actor on different domain than object")
        return result

    @property
    def object_id(self):
        """If the object has an object property, set to its id"""
        result = self.data.get("object")
        if isinstance(result, dict):
            return result.get("id")
        return result
