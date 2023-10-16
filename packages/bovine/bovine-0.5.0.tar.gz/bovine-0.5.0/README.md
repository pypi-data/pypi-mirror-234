# Bovine

Bovine is a basic utility library for the Fediverse. It can be used both to build ActivityPub Client applications and ActivityPub Servers. In addition to [ActivityPub](https://activitypub.rocks/) support, it also provides utilities to deal with [webfinger](https://webfinger.net), nodeinfo, and HTTP Signatures.

The bovine library can just be installed via pip

```bash
pip install bovine
```

Documentation including tutorials is available at [ReadTheDocs](https://bovine.readthedocs.io/en/latest/).
An entire working ActivityPub server can be found in the [bovine repository](https://codeberg.org/bovine/bovine/).

## Feedback

Issues about bovine should be filed as an [issue](https://codeberg.org/bovine/bovine/issues).

## Running BDD Tests

The following commands run the implemented BDD tests.

```bash
cd features
git clone https://codeberg.org/helge/fediverse-features.git
cd ..
behave -i http_signature
behave -i fep-4adb
```

## Contributing

If you want to contribute, you can start by working on issues labeled [Good first issue](https://codeberg.org/bovine/bovine/issues?q=&type=all&state=open&labels=110885&milestone=0&assignee=0&poster=0). The tech stack is currently based on asynchronous python, using the following components:

- [aiohttp](https://docs.aiohttp.org/en/stable/index.html) for http requests.
- [quart](https://quart.palletsprojects.com/en/latest/) as a webserver.
- [cryptography](https://cryptography.io/en/latest/).
- [pytest](https://docs.pytest.org/en/7.3.x/) for testing.
- [ruff](https://pypi.org/project/ruff/) for linting.
