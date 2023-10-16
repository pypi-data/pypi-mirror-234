import asyncio
import logging
from datetime import datetime, timedelta, timezone

from bovine.jsonld import combine_items
from bovine_store.models import StoredJsonObject, ObjectType
from bovine_store.utils.permissions import has_access

logger = logging.getLogger(__name__)


async def retrieve_object_by_id(retriever, object_id):
    result = await StoredJsonObject.get_or_none(id=object_id)

    if result is None:
        return None

    updated = result.updated
    updated = updated.replace(tzinfo=timezone.utc)

    if (
        updated < (datetime.now(tz=timezone.utc) - timedelta(days=1))
        and result.object_type == ObjectType.REMOTE
    ):
        logger.info("Object %s will be updated", object_id)
        # FIXME!

    if not await has_access(result, retriever):
        return None

    return result


async def retrieve_remote_object(retriever, object_id, include=[]):
    result = await retrieve_object_by_id(retriever, object_id)
    if result is None:
        return None

    data = result.content
    if len(include) == 0:
        return data

    items = await asyncio.gather(
        *[retrieve_object_by_id(retriever, data[key]) for key in include if key in data]
    )
    items = [obj.content for obj in items if obj]

    logger.debug("Retrieved %d items", len(items))

    return combine_items(data, items)
