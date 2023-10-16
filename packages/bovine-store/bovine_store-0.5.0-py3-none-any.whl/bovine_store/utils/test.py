import os
from dataclasses import dataclass
from unittest.mock import AsyncMock
import pytest
from tortoise import Tortoise, connections

from bovine_store import BovineStore, BovineAdminStore
from bovine_store.actor.bovine_store_actor import BovineStoreActor

db_file = "test_db.db"


async def init_connection(db_url):
    await Tortoise.init(db_url=db_url, modules={"models": ["bovine_store.models"]})
    await Tortoise.generate_schemas()


async def close_connection():
    await Tortoise.close_connections()


@dataclass
class EndpointMock:
    counter: int = 1

    def generate(self):
        self.counter += 1
        return f"https://my_domain/endpoints/{self.counter}"


def determine_db_url():
    db_url = os.environ.get("BOVINE_DB_URL")

    if db_url:
        return db_url

    return f"sqlite://{db_file}"


@pytest.fixture
async def store() -> BovineStore:
    """pytest fixture for a BovineStore if the environment variable
    `BOVINE_DB_URL` the db from it is used. The schema is created
    and dropped on each test. If the environment variable is not set
    a sqlite3 database is used, whose file is deleted after the test
    is finished."""
    response_mock = AsyncMock()
    response_mock.raise_for_status = lambda: 1
    session_mock = AsyncMock()
    session_mock.get.return_value = response_mock

    db_url = determine_db_url()
    store = BovineStore(
        db_url,
        session=session_mock,
    )
    await init_connection(db_url)

    yield store

    if os.environ.get("BOVINE_DB_URL"):
        connection = connections.get("default")
        for table in [
            "visibleto",
            "bovineactorendpoint",
            "bovineactorkeypair",
            "collectionitem",
            "storedjsonobject",
            "bovineactor",
        ]:
            await connection.execute_query(f"DROP TABLE IF EXISTS {table}")
        await close_connection()
    else:
        await close_connection()
        os.unlink(db_file)


@pytest.fixture
async def bovine_admin_store(store) -> BovineAdminStore:
    """Fixture for a bovine admin store, uses the same database as the store fixture."""
    endpoint_mock = EndpointMock()

    yield BovineAdminStore(
        determine_db_url(),
        endpoint_path_function=endpoint_mock.generate,
    )


@pytest.fixture
async def bovine_store_actor(store, bovine_admin_store) -> BovineStoreActor:
    """Creates and returns a BovineStoreActor"""
    bovine_name = await bovine_admin_store.register("MoonJumpingCow")

    yield await store.actor_for_name(bovine_name)
