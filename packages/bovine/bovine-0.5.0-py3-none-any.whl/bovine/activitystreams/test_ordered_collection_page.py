from . import OrderedCollectionPage


def test_ordered_collection_page() -> None:
    result = OrderedCollectionPage(
        id="url?page=1", part_of="url", items=["id1"]
    ).build()

    assert result == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "url?page=1",
        "partOf": "url",
        "orderedItems": ["id1"],
        "type": "OrderedCollectionPage",
    }

    result = OrderedCollectionPage(
        id="url?page=1", part_of="url", items=["id1"], next="next_url", prev="prev_url"
    ).build()

    assert result == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "url?page=1",
        "next": "next_url",
        "prev": "prev_url",
        "partOf": "url",
        "orderedItems": ["id1"],
        "type": "OrderedCollectionPage",
    }
