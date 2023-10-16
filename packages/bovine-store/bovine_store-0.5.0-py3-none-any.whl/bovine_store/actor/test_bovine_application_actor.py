from . import BovineApplicationActor


def test_bovine_application_actor():
    actor = BovineApplicationActor(
        {
            "account_url": "http://localhost:8080",
            "private_key": "private_key",
            "public_key": "public_key_pem",
        }
    )
    actor_object = actor.actor_object

    assert actor_object["id"] == "http://localhost:8080"
    assert actor_object["inbox"] == "http://localhost:8080"
    assert actor_object["outbox"] == "http://localhost:8080"
    assert actor_object["preferredUsername"] == "bovine"

    assert actor_object["publicKey"] == {
        "id": "http://localhost:8080#main-key",
        "owner": "http://localhost:8080",
        "publicKeyPem": "public_key_pem",
    }
