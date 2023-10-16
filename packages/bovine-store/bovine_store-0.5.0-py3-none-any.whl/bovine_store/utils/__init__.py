from bovine_store.types import EndpointType


def determine_summary(obj):
    for key in ["summary", "name", "content"]:
        if obj.get(key):
            return obj[key][:97]
    return


def get_actor_endpoint(endpoints):
    for endpoint in endpoints:
        if endpoint.endpoint_type == EndpointType.ACTOR:
            return endpoint


def get_account(keypairs):
    for kp in keypairs:
        if kp.public_key.startswith("acct:"):
            return kp


def user_to_account_and_actor_url(user):
    if not user:
        return None, None

    endpoint = get_actor_endpoint(user.endpoints)
    keypair = get_account(user.keypairs)

    return (keypair.public_key, endpoint.name)


def add_sub_collections(obj: dict) -> dict:
    """Adds the subcollections replies, shares, and likes to the
    object given by obj"""

    obj_type = obj.get("type")
    obj_id = obj.get("id")
    if obj_type not in ["Note", "Article", "Page"] or not obj_id:
        return obj

    for key in ["replies", "shares", "likes"]:
        obj[key] = f"{obj_id}/{key}"

    return obj
