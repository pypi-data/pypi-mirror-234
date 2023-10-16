import logging
import pytest

from bovine.jsonld import bovine_context_name
from bovine_store.utils.test import store  # noqa F401

from .store import store_remote_object


logger = logging.getLogger(__name__)


async def test_store_remote_object_like_stored(store):  # noqa F811
    first_id = "https://my_domain/first"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Like",
    }

    await store_remote_object("owner", item)

    first = await store.retrieve("owner", first_id)
    item["@context"] = bovine_context_name
    assert first == item


@pytest.mark.parametrize(
    "object_type",
    ["Collection", "OrderedCollection", "CollectionPage", "OrderedCollectionPage"],
)
async def test_store_remote_object_collections_are_not_stored(
    store, object_type  # noqa F811
):
    first_id = "https://my_domain/first"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": object_type,
    }

    await store_remote_object("owner", item)

    first = await store.retrieve("owner", first_id)
    assert first is None


async def test_store_remote_object_visible_to_many(store):  # noqa F811
    first_id = "https://my_domain/first"
    second_id = "https://my_domain/second"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
        "object": {"type": "Note", "id": second_id},
    }

    for j in range(10):
        await store_remote_object("owner", item, visible_to=[f"person_{j}"])

    first = await store.retrieve("owner", first_id)
    item["@context"] = bovine_context_name
    item["object"] = second_id

    assert first == item

    for j in range(10):
        first = await store.retrieve(f"person_{j}", first_id)
        item["@context"] = bovine_context_name
        assert first == item
