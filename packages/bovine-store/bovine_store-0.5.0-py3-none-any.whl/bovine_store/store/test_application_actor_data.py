from bovine_store.utils.test import store  # noqa F401
from bovine_store.models import BovineActor
from . import load_application_actor_data


async def test_load_application_actor_data(store):  # noqa F801
    base_data = {
        "private_key": "private_key",
        "public_key": "public_key_pem",
    }
    result = await load_application_actor_data(base_data)

    assert result == base_data
    assert 1 == await BovineActor.filter().count()

    result = await load_application_actor_data({})
    assert result == base_data
