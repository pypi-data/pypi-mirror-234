import aiohttp

from bovine_store.utils.test import store  # noqa F401

from .register import register
from .bovine_store_actor import BovineStoreActor


async def test_register(store):  # noqa: F811
    handle_name = "alice"
    async with aiohttp.ClientSession() as session:
        db_actor = await register(
            handle_name,
            endpoint_path="http://localhost:5000",
        )

        await db_actor.fetch_related("endpoints", "keypairs")

        db_actor.properties = {
            "name": "alyssa",
            "summary": "alice is alyssa",
            "icon": {
                "type": "Image",
                "mediaType": "image/png",
                "url": "http://localhost:5000/image.png",
            },
            "type": "Organization",
        }
        await db_actor.save()

        actor = await BovineStoreActor.from_database(db_actor, session)

        assert actor.actor_object.preferred_username == handle_name
        assert actor.actor_object.name == "alyssa"
        assert actor.actor_object.summary == "alice is alyssa"
        assert actor.actor_object.icon == {
            "type": "Image",
            "mediaType": "image/png",
            "url": "http://localhost:5000/image.png",
        }
        assert actor.actor_object.outbox != actor.actor_object.inbox
        assert actor.actor_object.type == "Organization"

        keypairs = db_actor.keypairs

        assert len(keypairs) == 2

        key_names = [kp.name for kp in keypairs]
        assert set(key_names) == {"account", "serverKey"}

        for kp in keypairs:
            if kp.name == "account":
                assert kp.public_key == "acct:alice@localhost:5000"
