from bovine_store.actor.bovine_store_actor import BovineStoreActor

from .test import store, bovine_admin_store, bovine_store_actor  # noqa F801


async def test_fixture_bovine_store_actor(bovine_store_actor):  # noqa F401
    assert isinstance(bovine_store_actor, BovineStoreActor)

    actor = bovine_store_actor.actor_object.build()

    assert actor["preferredUsername"] == "MoonJumpingCow"
