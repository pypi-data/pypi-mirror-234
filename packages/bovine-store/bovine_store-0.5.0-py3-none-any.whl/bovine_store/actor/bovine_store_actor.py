import asyncio
from datetime import datetime, timedelta, timezone
import logging
import traceback
import uuid
from urllib.parse import urljoin

from typing import Optional, List

from bovine import BovineActor
from bovine.activitystreams import Actor
from bovine.jsonld import combine_items

from bovine_store.store.store import store_remote_object
from bovine_store.store.remote import update_remote_object
from bovine_store.store.retrieve_object import retrieve_remote_object
from bovine_store.models import (
    StoredJsonObject,
    CollectionItem,
    BovineActor as DbBovineActor,
)
from bovine_store.types import EndpointType, ObjectType
from bovine_store.store.utils import domain_from_host
from bovine_store.store.collection import (
    collection_all,
    add_to_collection,
    remove_from_collection,
)

logger = logging.getLogger(__name__)


class BovineStoreActor(BovineActor):
    """Represents an actor controlled by bovine and stored in the database.
    This class should be used to perform actions as this actor. In particular,
    instances of this class are passed to bovine_process when performing
    side effects."""

    def __init__(
        self, actor_object: Actor, endpoints: List[str] = [], bovine_name=None, **config
    ):
        self.actor_object: Actor = actor_object
        self.bovine_name = bovine_name

        self.domain = domain_from_host(actor_object.id)
        self.endpoints = endpoints

        super().__init__(**config)

    async def retrieve_own_object(self, object_id: str) -> dict | None:
        """Retrieves an object owner by the actor"""
        result = await StoredJsonObject.get_or_none(id=object_id)
        if not result:
            return None
        if result.owner != self.actor_object.id:
            return None
        return result.content

    async def retrieve(
        self, object_id: str, include=[], skip_fetch: bool = False
    ) -> dict | None:
        """Retrieves the object with identified by object_id. The logic is
        as follows:

        * If object is in database and either local or remote and last updated
            in the last day, the object is returned from the database
        * Otherwise the object is fetched (as the actor) unless skip_fetch is set
        * Finally if include lists properties to be resolved, these objects
            are obtained using the above logic, and then added to the Object

        """
        if isinstance(object_id, dict):
            object_id = object_id.get("id")
        if not object_id:
            return None
        if len(object_id) > 255:
            logger.warning("Got too long object_id %s", object_id)
            return None

        data = await self._retrieve_object_from_database(
            object_id, skip_fetch=skip_fetch
        )

        if data is None:
            return data

        if len(include) == 0:
            return data

        items = await asyncio.gather(
            *[
                self._retrieve_object_from_database(data[key])
                for key in include
                if key in data
            ]
        )

        return combine_items(data, items)

    async def _retrieve_object_from_database(
        self, object_id, skip_fetch: bool = False
    ) -> Optional[dict]:
        if isinstance(object_id, dict):
            return object_id
        try:
            result = await StoredJsonObject.get_or_none(id=object_id)

            if skip_fetch:
                if result:
                    return result.content
                return None

            if not BovineStoreActor._is_stale(result):
                return result.content

            logger.info("Object %s is being refetched", object_id)

            obj = await self.get(object_id)
            if "attributedTo" in obj:
                owner = obj["attributedTo"]
            elif "actor" in obj:
                owner = obj["actor"]
            else:
                owner = object_id

            logger.info("Storing %s", obj["id"])

            await update_remote_object(
                owner,
                obj,
                visible_to=[self.actor_object.id],
                object_type=ObjectType.REMOTE,
            )

            return obj
        except Exception as ex:
            logger.info("Failed to retrieve %s with %s", object_id, ex)
            for log_line in traceback.format_exc().splitlines():
                logger.info(log_line)

            return None

    async def store(self, item: dict, as_public: bool = False, visible_to=[]):
        """Stores object in database"""
        return await store_remote_object(
            self.actor_id,
            item,
            as_public=as_public,
            visible_to=visible_to,
            object_type=ObjectType.LOCAL,
        )

    async def update(self, item: dict):
        """Updates object in database"""
        await update_remote_object(self.actor_object.id, item)

    async def retrieve_for(self, retriever, object_id, include=[]):
        return await retrieve_remote_object(retriever, object_id, include=include)

    async def store_for(self, owner: str, item: dict, as_public=False, visible_to=[]):
        """Stores a remote object

        :param owner: The actor who has submitted the object
        :param item: The object to store"""

        return await store_remote_object(
            owner, item, as_public=as_public, visible_to=visible_to, domain=self.domain
        )

    async def update_for(self, owner, item):
        return await update_remote_object(owner, item)

    async def add_to_outbox(self, object_id):
        return await add_to_collection(self.actor_object.outbox, object_id)

    async def add_to_inbox(self, object_id):
        return await add_to_collection(self.actor_object.inbox, object_id)

    async def add_to_followers(self, object_id):
        return await add_to_collection(self.actor_object.followers, object_id)

    async def remove_from_followers(self, object_id):
        return await remove_from_collection(self.actor_object.followers, object_id)

    async def add_to_following(self, object_id):
        return await add_to_collection(self.actor_object.following, object_id)

    async def remove_from_following(self, object_id):
        return await remove_from_collection(self.actor_object.following, object_id)

    async def add_to_interaction(
        self, interaction: str, object_id: str, remote_id: str
    ):
        """Adds to an interaction collection

        :param interaction:
            The interaction either replies, shares, or likes
        :param object_id:
            id of the object being interacted with
        :param remote_id:
            id of the interaction, e.g. of the Like or Dislike
        """
        return await add_to_collection(f"{object_id}/{interaction}", remote_id)

    async def remove_from_interaction(
        self, interaction: str, object_id: str, remote_id: str
    ):
        """Removes an interaction from the corresponding collection

        :param interaction:
            The interaction either replies, shares, or likes
        :param object_id:
            id of the object being interacted with
        :param remote_id:
            id of the interaction, e.g. of the Like or Dislike
        """
        obj = await CollectionItem.get_or_none(
            part_of=f"{object_id}/{interaction}", object_id=remote_id
        )
        if obj:
            await obj.delete()

    async def remove_references(self, remote_id: str):
        references = await CollectionItem.filter(
            part_of__endswith="replies", object_id=remote_id
        ).all()
        for reply in references:
            await reply.delete()

    async def resolve_endpoints(self, endpoints):
        tasks = [collection_all(self.actor_id, endpoint) for endpoint in endpoints]
        result = await asyncio.gather(*tasks)
        result = set(sum(result, []))

        logger.info("Resolved %s to %s", ", ".join(endpoints), ", ".join(result))
        return result

    def generate_new_object_id(self) -> str:
        """Creates a new object id

        This contains a hard coded path; probably should replace with something better.
        """
        return urljoin(self.actor_object.id, "/objects/" + str(uuid.uuid4()))

    async def update_profile(self, data: dict):
        """Updates the Actor profile"""

        database_actor = await DbBovineActor.get(bovine_name=self.bovine_name)
        database_actor.properties = data
        await database_actor.save()

    @staticmethod
    def _is_stale(result):
        if result is None:
            return True
        if result.object_type == ObjectType.LOCAL:
            return False

        updated = result.updated
        updated = updated.replace(tzinfo=timezone.utc)

        return updated < (datetime.now(tz=timezone.utc) - timedelta(days=1))

    @staticmethod
    async def from_database(stored_actor, session):
        """Creates BovineStoreAction from database object

        :param stored_actor:
            The BovineActor object from the database
        :param session:
            An aiohttp.ClientSession"""
        mapped_endpoints = {x.endpoint_type: x for x in stored_actor.endpoints}
        account_url = mapped_endpoints[EndpointType.ACTOR].name

        def get_server_key(stored_actor):
            for iter_keypair in stored_actor.keypairs:
                if iter_keypair.name == "serverKey":
                    return iter_keypair
            return stored_actor.keypairs[0]

        keypair = get_server_key(stored_actor)
        public_key_url = f"{account_url}#{keypair.name}"

        endpoints = [
            x.name
            for x in stored_actor.endpoints
            if x.endpoint_type in [EndpointType.FOLLOWERS, EndpointType.COLLECTION]
        ]

        actor_object = Actor(
            id=account_url,
            preferred_username=stored_actor.handle_name,
            inbox=mapped_endpoints[EndpointType.INBOX].name,
            outbox=mapped_endpoints[EndpointType.OUTBOX].name,
            event_source=mapped_endpoints[EndpointType.EVENT_SOURCE].name,
            followers=mapped_endpoints[EndpointType.FOLLOWERS].name,
            following=mapped_endpoints[EndpointType.FOLLOWING].name,
            proxy_url=mapped_endpoints[EndpointType.PROXY_URL].name,
            public_key=keypair.public_key,
            public_key_name=keypair.name,
        )

        if "type" in stored_actor.properties:
            actor_object.type = stored_actor.properties["type"]
        if "name" in stored_actor.properties:
            actor_object.name = stored_actor.properties["name"]
        if "summary" in stored_actor.properties:
            actor_object.summary = stored_actor.properties["summary"]
        if "icon" in stored_actor.properties:
            actor_object.icon = stored_actor.properties["icon"]
        if "url" in stored_actor.properties:
            actor_object.url = stored_actor.properties["url"]

        actor = BovineStoreActor(
            actor_object,
            endpoints=endpoints,
            bovine_name=stored_actor.bovine_name,
            actor_id=account_url,
            public_key_url=public_key_url,
            secret=keypair.private_key,
        )
        await actor.init(session=session)

        return actor
