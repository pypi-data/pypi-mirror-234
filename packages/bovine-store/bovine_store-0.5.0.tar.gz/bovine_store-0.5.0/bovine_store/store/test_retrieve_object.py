import json
from datetime import datetime, timedelta
from tortoise import connections
from bovine.jsonld import bovine_context_name

from bovine_store.utils.test import store  # noqa F401
from .store import store_remote_object
from .retrieve_object import retrieve_remote_object


async def test_store_retrieval(store):  # noqa F811
    first_id = "https://my_domain/first"
    second_id = "https://my_domain/second"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
        "object": {
            "type": "Note",
            "id": second_id,
        },
    }

    await store_remote_object("owner", item)

    first = await retrieve_remote_object("owner", first_id, include=["object"])

    item["@context"] = bovine_context_name
    assert first == item

    second = await retrieve_remote_object("owner", second_id, include=["object"])

    assert set(second.keys()) == {"@context", "type", "id"}


async def test_refetch_entries(store):  # noqa F401
    first_id = "https://my_domain/first"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Note",
        "id": first_id,
    }

    five_days_ago = datetime.utcnow() - timedelta(days=5)

    conn = connections.get("default")

    # Workaround auto_now from model
    await conn.execute_query(
        """INSERT INTO storedjsonobject
           (id, content, owner, updated, object_type)
        VALUES ($1, $2, $3, $4, $5)""",
        [first_id, json.dumps(item), "owner", five_days_ago, "REMOTE"],
    )

    result = await retrieve_remote_object("owner", first_id)

    assert result == item
