from bovine.crypto import generate_rsa_public_private_key
from bovine_store.models import BovineActor, BovineActorKeyPair

bovine_application_actor_name = "__bovine__application_actor__"


async def load_application_actor_data(data: dict) -> dict:
    if "access_token" in data:
        return data
    actor = await BovineActor.get_or_none(bovine_name=bovine_application_actor_name)
    if actor is None:
        actor, created = await BovineActor.update_or_create(
            bovine_name=bovine_application_actor_name,
            defaults={"handle_name": "bovine", "properties": {}},
        )
        if created:
            private_key = data.get("private_key")
            public_key = data.get("public_key")
            if not private_key or not public_key:
                public_key, private_key = generate_rsa_public_private_key()
            await BovineActorKeyPair.create(
                bovine_actor=actor,
                name="main-key",
                private_key=private_key,
                public_key=public_key,
            )
            return {"public_key": public_key, "private_key": private_key, **data}
        return data

    await actor.fetch_related("keypairs")

    for kp in actor.keypairs:
        if kp.name == "main-key":
            return {"private_key": kp.private_key, "public_key": kp.public_key}
    return data
