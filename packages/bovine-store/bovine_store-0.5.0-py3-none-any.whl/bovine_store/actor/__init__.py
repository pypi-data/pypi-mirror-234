import bovine
from bovine.activitystreams import Actor

from bovine_store.types import ObjectType
from bovine_store.store.store import store_remote_object
from bovine_store.store.retrieve_object import retrieve_remote_object


class BovineApplicationActor(bovine.BovineActor):
    """Actor that represents the bovine application,
    used when acting on behalf of a remote actor when the affected local
    actor is unknown.

    * Retrieving public keys for authorization checks
    """

    def __init__(self, config):
        super().__init__(
            actor_id=config["account_url"],
            public_key_url=config["account_url"] + "#main-key",
            secret=config["private_key"],
        )

        self.actor_object = Actor(
            id=config["account_url"],
            preferred_username="bovine",
            public_key=config["public_key"],
            public_key_name="main-key",
            type="Application",
        ).build()

    async def store_remote_actor(self, item):
        """Stores a remote actor. Actors are assumed to be publicly
        readable and to own themselves"""

        return await store_remote_object(
            item.get("id", "NO_OWNER"),
            item,
            as_public=True,
            visible_to=[self.actor_object["id"]],
            object_type=ObjectType.REMOTE,
        )

    async def retrieve(self, key_url):
        """retrieves a remote object form the database as the application actor"""
        return await retrieve_remote_object(self.actor_object["id"], key_url)
