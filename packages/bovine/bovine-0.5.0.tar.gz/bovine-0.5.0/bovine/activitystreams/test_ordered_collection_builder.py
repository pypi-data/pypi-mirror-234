from . import OrderedCollection


def test_ordered_collection_builder() -> None:
    result = OrderedCollection(id="url").build()

    assert result == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "url",
        "totalItems": 0,
        "type": "OrderedCollection",
    }


def test_ordered_collection_builder_with_items() -> None:
    result = OrderedCollection(id="url", count=1, items=[{"item": "1"}]).build()

    assert result == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "url",
        "orderedItems": [{"item": "1"}],
        "totalItems": 1,
        "type": "OrderedCollection",
    }


def test_ordered_collection_builder_with_fist_last() -> None:
    result = OrderedCollection(id="url", count=1, first="first", last="last").build()

    assert result == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "url",
        "first": "first",
        "last": "last",
        "totalItems": 1,
        "type": "OrderedCollection",
    }
