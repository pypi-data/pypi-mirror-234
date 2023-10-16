from tortoise import fields
from tortoise.models import Model

from .types import VisibilityTypes, ObjectType, EndpointType


class StoredJsonObject(Model):
    """Stores an object"""

    id = fields.CharField(max_length=255, pk=True)
    """The id of the object"""
    owner = fields.CharField(max_length=255)
    """The owner of the object, usually either

    * content["actor"]
    * content["attributedTo"]"""

    content = fields.JSONField()
    """content of the object as json"""

    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

    visibility = fields.CharEnumField(
        VisibilityTypes, default=VisibilityTypes.RESTRICTED
    )
    object_type = fields.CharEnumField(ObjectType, default=ObjectType.LOCAL)


class VisibleTo(Model):
    id = fields.IntField(pk=True)
    main_object = fields.ForeignKeyField(
        "models.StoredJsonObject", related_name="visible_to"
    )
    """Stored object, has foreign key"""
    object_id = fields.CharField(max_length=255)
    """id of the object that it is visible to"""


class CollectionItem(Model):
    id = fields.IntField(pk=True)
    """id of the collection, an integer, used for pagination"""

    part_of = fields.CharField(max_length=255)
    """id of the collection"""
    object_id = fields.CharField(
        max_length=255,
    )
    """id of the element in the collection"""

    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

    class Meta:
        unique_together = (("part_of", "object_id"),)


class BovineActor(Model):
    id = fields.IntField(pk=True)
    bovine_name = fields.CharField(max_length=255, unique=True)
    """Internally used name to identify the actor --- unique"""
    handle_name = fields.CharField(max_length=255)
    """The preferred user name - not necessarily unique

    unsure if really necessary here"""

    properties = fields.JSONField()
    """Additional properties of the actor

    For example: name, url or icon. Currently arbitrary properties
    are not allowed yet, but should be in the future. Some thinking
    is needed here how to handle the context and so on."""

    created = fields.DatetimeField(auto_now_add=True)
    last_sign_in = fields.DatetimeField(auto_now=True)


class BovineActorEndpoint(Model):
    id = fields.IntField(pk=True)

    bovine_actor = fields.ForeignKeyField(
        "models.BovineActor", related_name="endpoints"
    )
    """The actor this endpoint belongs to"""

    endpoint_type = fields.CharEnumField(enum_type=EndpointType)
    """type of the endpoint, e.g. endpoint"""

    stream_name = fields.CharField(max_length=255)
    """Human readable name of the endpoint"""

    name = fields.CharField(max_length=255)
    """The url the endpoint points to"""


class BovineActorKeyPair(Model):
    """
    Represents identifiers associated with the actor. It contains currently
    a mix of identities. These are:

    * server key, e.g. RSA key pair for HTTP Signatures
    * identifiers used to lookup the actor, e.g. acct:handle@domain
    * did keys used to identify one is a BovineClient

    FIXME: Do we need a type, an order, a should display? Think about these things
    https://socialhub.activitypub.rocks/t/alsoknownas-and-acct/3132?u=helge
    """

    id = fields.IntField(pk=True)

    bovine_actor = fields.ForeignKeyField("models.BovineActor", related_name="keypairs")
    """The actor this keypair belongs to"""

    name = fields.CharField(max_length=255)
    """Human readable name"""

    private_key = fields.TextField(null=True)  # FIXME Rename to secret
    """the secret in the keypair. The private_key is null if the keypair
    is used to gain access to the Actor from a Client"""

    public_key = fields.TextField()  # FIXME Rename to identity, Make unique
    """the public key"""
