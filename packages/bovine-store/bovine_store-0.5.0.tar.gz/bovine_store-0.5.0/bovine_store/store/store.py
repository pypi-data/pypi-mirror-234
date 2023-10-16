import asyncio
import logging

from bovine.jsonld import split_into_objects, with_bovine_context
from bovine_store.models import StoredJsonObject, VisibilityTypes, VisibleTo, ObjectType

from .utils import determine_object_type


logger = logging.getLogger(__name__)


def should_store(obj):
    if "type" not in obj:
        return True

    if obj["type"] in [
        "Collection",
        "OrderedCollection",
        "CollectionPage",
        "OrderedCollectionPage",
    ]:
        return False

    return True


async def safe_visible_create(item, actor):
    try:
        await VisibleTo.get_or_create(
            main_object=item,
            object_id=actor,
        )
    except Exception as ex:
        logger.warning(ex)
        logger.warning("Deleting entries and recreating")

        await VisibleTo.filter(main_object=item, object_id=actor).delete()
        await VisibleTo.get_or_create(
            main_object=item,
            object_id=actor,
        )
        logger.warning("Success for (%s, %s)", item, actor)


async def store_public_object(
    owner: str, item: dict, domain: str = "localhost", object_type: ObjectType = None
):
    to_store = await split_into_objects(item)

    to_store = [with_bovine_context(data) for data in to_store]

    objects = [
        StoredJsonObject(
            id=obj["id"],
            content=obj,
            owner=owner,
            visibility=VisibilityTypes.PUBLIC,
            object_type=determine_object_type(object_type, obj["id"], domain),
        )
        for obj in to_store
        if should_store(obj) and obj.get("id")
    ]
    return await StoredJsonObject.bulk_create(objects, ignore_conflicts=True)


async def store_remote_object(
    owner: str,
    item: dict,
    as_public: bool = False,
    visible_to=[],
    domain: str = "localhost",
    object_type: ObjectType = None,
):
    visibility_type = VisibilityTypes.RESTRICTED
    if as_public:
        return await store_public_object(
            owner, item, domain=domain, object_type=object_type
        )

    to_store = await split_into_objects(item)
    to_store = [with_bovine_context(data) for data in to_store]

    tasks = [
        StoredJsonObject.get_or_create(
            id=obj["id"],
            defaults={
                "content": obj,
                "owner": owner,
                "visibility": visibility_type,
                "object_type": determine_object_type(object_type, obj["id"], domain),
            },
        )
        for obj in to_store
        if should_store(obj) and obj.get("id")
    ]

    items = await asyncio.gather(*tasks)
    id_to_store = {obj["id"]: obj for obj in to_store if obj.get("id")}

    for item, created in items:
        visible_tasks = [safe_visible_create(item, actor) for actor in visible_to]
        await asyncio.gather(*visible_tasks)
        if not created:
            if item.owner == owner:
                item.content = id_to_store[item.id]
                await item.save()

                # FIXME visibility not changed; check timestamps?

    return items
