from typing import Optional
from urllib.parse import urlparse

from bovine_store.models import ObjectType


def domain_from_host(host: Optional[str]) -> str:
    if host is None:
        return "localhost"
    try:
        return urlparse(host).netloc
    except Exception:
        return "localhost"


def determine_object_type(
    object_type: Optional[ObjectType], object_id: str, domain: str
) -> ObjectType:
    if object_type:
        return object_type

    if urlparse(object_id).netloc == domain:
        return ObjectType.LOCAL
    else:
        return ObjectType.REMOTE
