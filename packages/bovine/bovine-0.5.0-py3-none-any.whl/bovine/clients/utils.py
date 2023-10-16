from importlib.metadata import version
from urllib.parse import urlparse

BOVINE_CLIENT_NAME = "bovine/" + version("bovine")


def host_target_from_url(url):
    parsed_url = urlparse(url)

    path = parsed_url.path
    if parsed_url.query:
        path = f"{path}?{parsed_url.query}"
    return parsed_url.netloc, path
