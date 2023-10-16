from urllib.parse import urljoin, urlparse
import secrets
import uuid

from typing import Callable

from bovine.crypto import generate_rsa_public_private_key

from bovine_store.models import BovineActor, BovineActorEndpoint, BovineActorKeyPair
from bovine_store.types import EndpointType


async def register(
    handle_name: str,
    endpoint_path: str | None = None,
    endpoint_path_function: Callable = None,
):
    if not endpoint_path_function:

        def random_endpoint():
            return urljoin(endpoint_path, secrets.token_urlsafe(32))

        endpoint_path_function = random_endpoint

    bovine_name = handle_name + "_" + str(uuid.uuid4())

    actor = await BovineActor.create(
        bovine_name=bovine_name,
        handle_name=handle_name,
        properties={},
    )
    await add_key_pair(actor, "serverKey")

    for endpoint_type in EndpointType:
        if endpoint_type != EndpointType.COLLECTION:
            await BovineActorEndpoint.create(
                bovine_actor=actor,
                endpoint_type=endpoint_type,
                name=endpoint_path_function(),
                stream_name=endpoint_type.value,
            )
    await add_account_handle(actor, handle_name, endpoint_path_function)

    return actor


async def add_key_pair(actor: BovineActor, name: str):
    public_key, private_key = generate_rsa_public_private_key()
    await BovineActorKeyPair.create(
        bovine_actor=actor, name=name, public_key=public_key, private_key=private_key
    )


async def add_account_handle(
    actor: BovineActor, handle_name: str, endpoint_path_function: Callable
):
    domain = urlparse(endpoint_path_function()).netloc

    account = f"acct:{handle_name}@{domain}"

    await BovineActorKeyPair.create(
        bovine_actor=actor,
        name="account",
        public_key=account,
    )
