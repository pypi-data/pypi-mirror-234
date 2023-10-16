from bovine_store.utils.test import store  # noqa F401

from . import BovineAdminStore


async def test_creation_with_domain(store):  # noqa F801
    store = BovineAdminStore(domain="example.com")

    await store.register("handle_name")

    assert store.endpoint_path == "https://example.com/endpoints/template"
