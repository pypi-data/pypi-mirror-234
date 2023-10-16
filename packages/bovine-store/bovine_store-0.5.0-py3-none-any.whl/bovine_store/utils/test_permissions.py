from bovine_store.models import CollectionItem, StoredJsonObject, VisibleTo
from bovine_store.utils.test import store  # noqa F401

from .permissions import has_access


async def test_has_access_for_owner(store):  # noqa F811
    entry = await StoredJsonObject.create(id="first", owner="owner", content={})

    assert await has_access(entry, "owner")
    assert not await has_access(entry, "other")


async def test_has_access_for_other_in_list(store):  # noqa F811
    entry = await StoredJsonObject.create(id="first", owner="owner", content={})

    await VisibleTo.create(main_object=entry, object_id="list")
    await CollectionItem.create(part_of="list", object_id="other")

    assert await has_access(entry, "other")
