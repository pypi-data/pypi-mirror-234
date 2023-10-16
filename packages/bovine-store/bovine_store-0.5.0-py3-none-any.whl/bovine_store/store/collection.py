import logging

from tortoise import connections

from bovine_store.models import CollectionItem

logger = logging.getLogger(__name__)


async def add_to_collection(collection_id, object_id):
    logger.debug("Adding %s to %s", object_id, collection_id)

    item = CollectionItem(part_of=collection_id, object_id=object_id)
    await CollectionItem.bulk_create([item], ignore_conflicts=True)

    return item


async def remove_from_collection(collection_id, object_id):
    item = await CollectionItem.get_or_none(part_of=collection_id, object_id=object_id)

    if item is None:
        return False

    await item.delete()

    return True


sql_joined_tables = """FROM collectionitem ci
JOIN storedjsonobject obj
    ON ci.object_id = obj.id
LEFT JOIN visibleto vis
    ON vis.main_object_id = ci.object_id
LEFT JOIN collectionitem follow
    ON vis.object_id = follow.part_of
"""
sql_where = """WHERE ci.part_of = $1
AND ( TRUE OR (
  obj.owner = $2 OR
  obj.visibility = 'PUBLIC'
  OR vis.object_id = $3
  OR (follow.object_id = $4
    AND (follow.created < obj.updated)
  ))
)
"""


async def collection_count(retriever, collection_id):
    return await CollectionItem.filter(part_of=collection_id).count()

    # sql_query = f"""SELECT COUNT (DISTINCT ci.object_id)
    #     {sql_joined_tables}
    #     {sql_where}
    # """
    # result = await client.execute_query_dict(
    #     sql_query, (collection_id, retriever, retriever, retriever)
    # )
    # if "count" in result[0]:
    #     return result[0]["count"]
    # return result[0]["COUNT (DISTINCT ci.object_id)"]


async def collection_items(retriever, collection_id, **kwargs) -> dict | None:
    limit = int(kwargs.get("limit", 10))

    query = CollectionItem.filter(part_of=collection_id)

    if kwargs.get("last"):
        query = query.order_by("id")
    elif kwargs.get("first"):
        query = query.order_by("-id")
    elif kwargs.get("min_id"):
        min_id = int(kwargs.get("min_id"))
        query = query.filter(id__lt=min_id).order_by("-id")
    elif kwargs.get("max_id"):
        max_id = int(kwargs.get("max_id"))
        query = query.filter(id__gt=max_id).order_by("id")

    result = await query.limit(limit).all()

    next_prev = {}
    if len(result) > 0:
        min_id = max(x.id for x in result)
        max_id = min(x.id for x in result)
        next_prev = {
            "prev": f"max_id={min_id}",
            "next": f"min_id={max_id}",
        }
    result = sorted(result, key=lambda x: -x.id)

    return {"items": [x.object_id for x in result], **next_prev}

    return result

    # sql_query = f"""SELECT DISTINCT ci.id, ci.object_id
    #     {sql_joined_tables}
    #     {sql_where}
    # """

    # query_args = [collection_id, retriever, retriever, retriever]

    # if kwargs.get("last"):
    #     sql_query = f"{sql_query} ORDER BY ci.id ASC"
    # elif kwargs.get("first"):
    #     sql_query = f"{sql_query} ORDER BY ci.id DESC"
    # elif kwargs.get("min_id"):
    #     min_id = int(kwargs.get("min_id"))
    #     sql_query = f"{sql_query} AND ci.id < $5"
    #     query_args.append(min_id)
    #     sql_query = f"{sql_query} ORDER BY ci.id DESC"
    # elif kwargs.get("max_id"):
    #     max_id = int(kwargs.get("max_id"))
    #     sql_query = f"{sql_query} AND ci.id > $5"
    #     query_args.append(max_id)
    #     sql_query = f"{sql_query} ORDER BY ci.id ASC"

    # sql_query = f"{sql_query} LIMIT {limit}"
    # client = connections.get("default")

    # result = await client.execute_query_dict(sql_query, query_args)
    # next_prev = {}
    # if len(result) > 0:
    #     min_id = max(x["id"] for x in result)
    #     max_id = min(x["id"] for x in result)
    #     next_prev = {
    #         "prev": f"max_id={min_id}",
    #         "next": f"min_id={max_id}",
    #     }
    # result = sorted(result, key=lambda x: -x["id"])

    # return {"items": [x["object_id"] for x in result], **next_prev}


async def collection_all(retriever, collection_id) -> list:
    items = await CollectionItem.filter(part_of=collection_id).all()
    return [item.object_id for item in items]

    sql_query = f"""SELECT ci.id, ci.object_id
        {sql_joined_tables}
        {sql_where}
    """

    query_args = [collection_id, retriever, retriever, retriever]

    client = connections.get("default")
    result = await client.execute_query_dict(sql_query, query_args)

    return [x["object_id"] for x in result]
