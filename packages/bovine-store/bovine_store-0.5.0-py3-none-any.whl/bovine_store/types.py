from enum import Enum


class VisibilityTypes(Enum):
    PUBLIC = "PUBLIC"
    RESTRICTED = "RESTRICTED"


class ObjectType(Enum):
    LOCAL = "LOCAL"
    REMOTE = "REMOTE"
    LOCAL_COLLECTION = "LOCAL_COLLECTION"
    DELETED = "DELETED"


class EndpointType(Enum):
    ACTOR = "ACTOR"
    INBOX = "INBOX"
    OUTBOX = "OUTBOX"
    FOLLOWERS = "FOLLOWERS"
    FOLLOWING = "FOLLOWING"

    PROXY_URL = "PROXY_URL"
    EVENT_SOURCE = "EVENT_SOURCE"

    COLLECTION = "COLLECTION"
