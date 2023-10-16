import json
from datetime import datetime, timedelta
from unittest.mock import patch, AsyncMock

from tortoise import connections

from bovine.activitystreams import Actor
from bovine.jsonld import bovine_context_name

from bovine_store.utils.test import store, bovine_store_actor  # noqa F401
from bovine_store.store.store import store_remote_object

from .bovine_store_actor import BovineStoreActor


@patch("bovine.clients.signed_http_methods.signed_get")
async def test_bovine_store_actor_retrieve(mock_signed_get, store):  # noqa F811
    actor = BovineStoreActor(
        Actor(id="local_id"),
        actor_id="http://my_host/endpoints/actor",
        public_key_url="localhost#key",
        secret="private_key",
    )
    response = AsyncMock()
    mock_signed_get.return_value = response
    response.raise_for_status = lambda: 1
    response.status = 200
    response.text.return_value = json.dumps(
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": "https://example.com/object_id",
            "type": "Note",
            "content": "I'll be stored",
        }
    )

    await actor.init()

    result = await actor.retrieve("https://example.com/object_id")
    mock_signed_get.assert_awaited_once()

    assert result

    result = await actor.retrieve("https://example.com/object_id")
    mock_signed_get.assert_awaited_once()

    assert result

    await actor.session.close()


async def test_bovine_store_actor_retrieval(store):  # noqa F811
    actor = BovineStoreActor(
        Actor(id="owner"),
        actor_id="http://my_host/endpoints/actor",
        public_key_url="localhost#key",
        secret="private_key",
    )

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

    first = await actor.retrieve(first_id, include=["object"])

    item["@context"] = bovine_context_name
    assert first == item

    second = await actor.retrieve(second_id, include=["object"])

    assert set(second.keys()) == {"@context", "type", "id"}


@patch("bovine.clients.signed_http_methods.signed_get")
async def test_refetch_entries(mock_signed_get, store):  # noqa F401
    actor = BovineStoreActor(
        Actor(id="owner"),
        actor_id="http://my_host/endpoints/actor",
        public_key_url="localhost#key",
        secret="private_key",
    )
    response = AsyncMock()
    mock_signed_get.return_value = response
    response.raise_for_status = lambda: 1
    response.status = 200
    first_id = "https://my_domain/first"

    stored_item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Note",
        "content": "I'll be stored",
    }
    response.text.return_value = json.dumps(stored_item)

    await actor.init()

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

    result = await actor.retrieve(first_id)

    assert result == stored_item

    mock_signed_get.assert_awaited_once()

    result = await actor.retrieve(first_id)

    assert result == stored_item

    mock_signed_get.assert_awaited_once()


@patch("bovine.clients.signed_http_methods.signed_get")
async def test_lookup_fails(mock_signed_get, store):  # noqa F401
    actor = BovineStoreActor(
        Actor(id="owner"),
        actor_id="http://my_host/endpoints/actor",
        public_key_url="localhost#key",
        secret="private_key",
    )
    response = AsyncMock()
    mock_signed_get.return_value = response
    response.raise_for_status = lambda: 1

    first_id = "https://my_domain/first"
    second_id = "https://my_domain/second"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
        "object": second_id,
    }

    await store_remote_object("owner", item)

    response.text.return_value = "NO NO NO"

    await actor.init()

    result = await actor.retrieve(first_id, include=["object"])

    item["@context"] = bovine_context_name
    assert result == item

    mock_signed_get.assert_awaited_once()


async def test_bovine_store_actor_object_id(store):  # noqa F811
    actor = BovineStoreActor(
        Actor(id="http://my_host/endpoints/actor"),
        actor_id="http://my_host/endpoints/actor",
        public_key_url="localhost#key",
        secret="private_key",
    )

    object_id = actor.generate_new_object_id()

    assert object_id.startswith("http://my_host/objects/")
