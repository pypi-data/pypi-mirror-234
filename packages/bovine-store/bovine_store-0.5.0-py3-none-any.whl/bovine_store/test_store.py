from bovine_store.utils.test import store  # noqa F401

from .actor import BovineApplicationActor
from . import BovineStore


async def test_application_actor(store):  # noqa F801
    store = BovineStore(
        application_data={"public_key": "public_key", "private_key": "private_key"}
    )

    application_actor = await store.application_actor_for_url(
        "https://my_domain/some/other/path"
    )

    assert isinstance(application_actor, BovineApplicationActor)
