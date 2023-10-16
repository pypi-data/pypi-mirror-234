from bovine_store import BovineStore
from contextlib import asynccontextmanager


@asynccontextmanager
async def bovine_actor(body, session):
    store = BovineStore(session=session)

    actor = await store.actor_for_name(body["bovine_name"])

    try:
        yield actor
    finally:
        ...
